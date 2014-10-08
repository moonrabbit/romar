# -*-coding:utf8-*-
import re
import copy

_field_regex = '\$\{([a-zA-Z0-9_]+)\}'
_field_regex_with_type = '\$\{([a-zA-Z0-9_]+?):([a-zA-Z0-9:<>]+)\}'
_list_type_regex = 'list<([a-z]+)>'

_default_options = {
    'list_separators': ', ',
    'ignore_empty_item': True,
    'filter': {}
}


def marshall_rows(rows, template, options=None, name_row_idx=1):
    fieldnames = rows[name_row_idx-1]
    fieldnames = [name.strip() for name in fieldnames]
    rows = rows[name_row_idx:]

    rawitems = []
    for row in rows:
        item = {}
        for idx, col in enumerate(row):
            item[fieldnames[idx]] = col
        rawitems.append(item)

    return marshall(rawitems, template, options)


def marshall(rawitems, template, options=None):
    tmp = options
    options = copy.copy(_default_options)
    if tmp is not None:
        options.update(tmp)
    filtered_items = _get_filtered_items(rawitems, options)

    result = None
    if type(template) is dict:
        result = {}
        for rawitem in filtered_items:
            templated_item = _marshall_item(rawitem, template, options)
            result.update(templated_item)
        return result
    elif type(template) is list:
        result = []
        for rawitem in filtered_items:
            templated_item = _marshall_item(rawitem, template[0], options)
            result.append(templated_item)
    return result


def _marshall_item(rawitem, template, options):
    if type(template) is dict:
        result = {}
        for key, value in template.items():
            nkey = _marshall_item(rawitem, key, options)
            nvalue = _marshall_item(rawitem, value, options)
            if (nkey is not None) and (nvalue is not None):
                result[nkey] = nvalue
        return result

    elif type(template) is list:
        result = []
        for value in template:
            nvalue = _marshall_item(rawitem, value, options)
            if nvalue is not None:
                result.append(nvalue)
        return result

    elif type(template) in (str, unicode):
        if _is_field(template):
            name, ftype = _get_field_comps(template)
            if name in rawitem:
                value = rawitem[name]
            else:
                return None
            if options['ignore_empty_item'] and len(value.strip()) == 0:
                return None
            value = _convert_to(ftype, value, options)
            return value
        elif options['ignore_empty_item'] and len(template.strip()) == 0:
                return None

    return template


def _get_filtered_items(rawitems, options):
    filter_data = options['filter']

    def filter_func(item):
        for key, value in filter_data.items():
            if _is_field(key):
                name, type = _get_field_comps(key)
                key = _convert_to(type, item[name], options)
            if _is_field(value):
                name, type = _get_field_comps(value)
                value = _convert_to(type, item[name], options)
            if key != value:
                return False
        return True
    return filter(filter_func, rawitems)


def _convert_to(type, value, options):
    ''' value를 type형으로 바꿔서 리턴한다.'''
    if type == 'str':
        return value
    elif type == 'num':
        value = value.replace('%', '')
        if '.' in value:
            return float(value)
        else:
            return int(value)
    elif type == 'bool':
        return value.lower() in ['y', 'ture', '1', 'yes']

    match = re.match(_list_type_regex, value)
    if match:
        separator = options['list_separators']
        itype = match.group(1)
        result = []
        items = re.split(separator, value)
        for item in items:
            item = item.strip()
            converted = _convert_to(itype, item, options)
            result.append(converted)
        return result


def _is_field(value):
    if type(value) not in (str, unicode):
        return False
    return re.match(_field_regex, value) \
        or re.match(_field_regex_with_type, value)


def _get_field_comps(string):
    match = re.match(_field_regex, string)
    if match:
        return match.group(1), 'str'

    match = re.match(_field_regex_with_type, string)
    if match:
        return ("%s:%s" % (match.group(1), match.group(2))), match.group(2)
