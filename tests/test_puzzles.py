import os
import unittest
import json
from unittest import TestCase


class TestPuzzles(TestCase):
    def setUp(self):
        with open("resources" + os.sep + "test_puzzles.json") as json_data:
            self.puzzle_json = json.load(json_data)

    def test_puzzles(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split('2')


if __name__ == '__main__':
    unittest.main()
