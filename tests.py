# coding=utf-8
import unittest
from main import Command


class TestMashtab(unittest.TestCase):
    def setUp(self):
        self.command = Command('module1', 'test1', 'foo1')
        self.rows = [
            ['module2', 'test2', 'foo0', False],
            ['module1', 'test1', 'foo1', True],
            ['module2', 'test3', 'foo4', False],
        ]
        self.names = ['user{}'.format(number) for number in range(1, 100)]

    def test_equal(self):
        for row in self.rows:
            command = Command(*row[:3])
            if row[3]:
                self.assertEqual(command, self.command)
            else:
                self.assertNotEqual(command, self.command)

    def test_add_user(self):
        for user_name in self.names:
            self.command.add_param(user_name)
        for user_name in ['user1']*100:
            self.command.add_param(user_name)
        self.assertTrue(len(self.command.param) == len(self.names))

    def test_get_dict_command(self):
        self.command.add_param('user1')
        self.assertEqual(self.command.get_dict_command(), {
            'module': 'module1',
            'name': 'test1',
            'function': 'foo1',
            'param': [
                'user1',
            ]
        })
        self.command.add_param('user2')
        self.assertEqual(self.command.get_dict_command(), {
            'module': 'module1',
            'name': 'test1',
            'function': 'foo1',
            'param': [
                'user1',
                'user2'
            ]
        })


if __name__ == '__main__':
    unittest.main()
