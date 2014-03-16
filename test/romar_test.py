import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))

import unittest
import romar


class MarshallTest(unittest.TestCase):
    options = {
        'filter':
        {
            '${inclusion:bool}': True
        },
        'list_separators': ", ",
        'ignore_empty_item': True
    }
    template_data = [{
        'id': '${id:str}',
        'stat':
        {
            'power': '${power:num}',
            '${stat_key_1:str}': '${stat_value_1:num}',
            '${stat_key_2:str}': '${stat_value_2:num}',
            '${stat_key_3:str}': '${stat_value_3:num}'
        },
        'tags':
        [
            '${tag_1:str}',
            '${tag_2:str}',
            '${tag_3:str}'
        ],
    }]

    def test_marshall(self):
        rawitems = [
            {
                'inclusion:bool': 'Y',
                'id:str': 'items_1',
                'power:num': '123.2',
                'stat_key_1:str': 'speed',
                'stat_value_1:num': '12',
                'stat_key_2:str': 'cooltime',
                'stat_value_2:num': '123.12',
                'stat_key_3:str': '          ',
                'tag_1:str': 'little',
                'tag_2:str': 'big'
            },
            {
                'inclusion:bool': 'Y',
                'id:str': 'items_2',
                'power:num': '321'
            },
            {
                'inclusion:bool': 'N',
                'id:str': 'items_3',
                'power:num': '321'
            }
        ]

        correct_result = [
            {
                'id': 'items_1',
                'stat':
                {
                    'power': 123.2,
                    'speed': 12,
                    'cooltime': 123.12
                },
                'tags': ['little', 'big']
            },
            {
                'id': 'items_2',
                'stat':
                {
                    'power': 321
                },
                'tags': []
            }
        ]

        result = romar.marshall(rawitems, self.template_data, self.options)
        self.assertEqual(result, correct_result)

    def test_marshall_rows(self):
        correct_result = [
            {
                'id': 'items_1',
                'stat':
                {
                    'power': 123.2,
                    'speed': 12,
                    'cooltime': 123.12
                },
                'tags': ['little', 'big']
            },
            {
                'id': 'items_2',
                'stat':
                {
                    'power': 321
                },
                'tags': []
            }
        ]

        rows = [
            [
                'inclusion:bool', 'id:str', 'power:num',
                'stat_key_1:str', 'stat_value_1:num',
                'stat_key_2:str', 'stat_value_2:num',
                'stat_key_3:str', 'stat_value_3:num',
                'tag_1:str', 'tag_2:str', 'tag_3:str'
            ],
            [
                'Y', 'items_1', '123.2',
                'speed', '12',
                'cooltime', '123.12',
                '', '',
                'little', 'big', ''
            ],
            [
                'Y', 'items_2', '321',
                '', '',
                '', '',
                '', '',
                '', '', ''
            ],
            [
                'N', 'items_3', '321',
                '', '',
                '', '',
                '', '',
                '', '', ''
            ],
        ]

        result = romar.marshall_rows(
            rows, self.template_data, self.options)
        self.assertEqual(result, correct_result)

if __name__ == '__main__':
    unittest.main()
