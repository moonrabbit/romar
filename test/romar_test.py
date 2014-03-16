import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), u'../'))

import unittest
import romar


class MarshallTest(unittest.TestCase):
    options = {
        u'filter':
        {
            u'${inclusion:bool}': True
        },
        u'list_separators': u', ',
        u'ignore_empty_item': True
    }
    template_data = [{
        u'id': u'${id:str}',
        u'stat':
        {
            u'power': u'${power:num}',
            u'${stat_key_1:str}': u'${stat_value_1:num}',
            u'${stat_key_2:str}': u'${stat_value_2:num}',
            u'${stat_key_3:str}': u'${stat_value_3:num}'
        },
        u'tags':
        [
            u'${tag_1:str}',
            u'${tag_2:str}',
            u'${tag_3:str}'
        ],
    }]

    def test_marshall(self):
        rawitems = [
            {
                u'inclusion:bool': u'Y',
                u'id:str': u'items_1',
                u'power:num': u'123.2',
                u'stat_key_1:str': u'speed',
                u'stat_value_1:num': u'12',
                u'stat_key_2:str': u'cooltime',
                u'stat_value_2:num': u'123.12',
                u'stat_key_3:str': u'          u',
                u'tag_1:str': u'little',
                u'tag_2:str': u'big'
            },
            {
                u'inclusion:bool': u'Y',
                u'id:str': u'items_2',
                u'power:num': u'321'
            },
            {
                u'inclusion:bool': u'N',
                u'id:str': u'items_3',
                u'power:num': u'321'
            }
        ]

        correct_result = [
            {
                u'id': u'items_1',
                u'stat':
                {
                    u'power': 123.2,
                    u'speed': 12,
                    u'cooltime': 123.12
                },
                u'tags': ['little', u'big']
            },
            {
                u'id': u'items_2',
                u'stat':
                {
                    u'power': 321
                },
                u'tags': []
            }
        ]

        result = romar.marshall(rawitems, self.template_data, self.options)
        self.assertEqual(result, correct_result)

    def test_marshall_rows(self):
        correct_result = [
            {
                u'id': u'items_1',
                u'stat':
                {
                    u'power': 123.2,
                    u'speed': 12,
                    u'cooltime': 123.12
                },
                u'tags': ['little', u'big']
            },
            {
                u'id': u'items_2',
                u'stat':
                {
                    u'power': 321
                },
                u'tags': []
            }
        ]

        rows = [
            [
                u'inclusion:bool', u'id:str', u'power:num',
                u'stat_key_1:str', u'stat_value_1:num',
                u'stat_key_2:str', u'stat_value_2:num',
                u'stat_key_3:str', u'stat_value_3:num',
                u'tag_1:str', u'tag_2:str', u'tag_3:str'
            ],
            [
                u'Y', u'items_1', u'123.2',
                u'speed', u'12',
                u'cooltime', u'123.12',
                u'', u'',
                u'little', u'big', u''
            ],
            [
                u'Y', u'items_2', u'321',
                u'', u'',
                u'', u'',
                u'', u'',
                u'', u'', u''
            ],
            [
                u'N', u'items_3', u'321',
                u'', u'',
                u'', u'',
                u'', u'',
                u'', u'', u''
            ],
        ]

        result = romar.marshall_rows(
            rows, self.template_data, self.options)
        self.assertEqual(result, correct_result)

if __name__ == u'__main__':
    unittest.main()
