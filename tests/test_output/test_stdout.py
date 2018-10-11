#!/usr/bin/env python

import collections
import io
import textwrap
import unittest

from gitem import output


class TestStdout(unittest.TestCase):

    @staticmethod
    def dedent_helper(s):
        return textwrap.dedent(s).lstrip()

    def test_basic(self):
        data = collections.OrderedDict([
            ('key', 'value'),
        ])

        with io.StringIO() as stream:
            outputter = output.Stdout(file_=stream)
            outputter.output(data)
            result = stream.getvalue()

        expected = self.dedent_helper('''
            key: value
        ''')

        self.assertEqual(result, expected)

    def test_list(self):
        data = collections.OrderedDict([
            ('key1', collections.OrderedDict([
                ('key2', ['value1', 'value2']),
            ])),
        ])

        with io.StringIO() as stream:
            outputter = output.Stdout(file_=stream)
            outputter.output(data)
            result = stream.getvalue()

        expected = self.dedent_helper('''
            key1:
              key2:
                value1
                value2
        ''')

        self.assertEqual(result, expected)

    def test_recurse(self):
        data = collections.OrderedDict([
            ('key1', 'value1'),
            ('key2', collections.OrderedDict([
                ('key3', 'value2'),
            ])),
        ])

        with io.StringIO() as stream:
            outputter = output.Stdout(file_=stream)
            outputter.output(data)
            result = stream.getvalue()

        expected = self.dedent_helper('''
            key1: value1

            key2:
              key3: value2
        ''')

        self.assertEqual(result, expected)

    def test_newline(self):
        data = collections.OrderedDict([
            ('key1', 'value1'),
            ('key2', collections.OrderedDict([
                ('key3', 'value2'),
            ])),
            ('key4', collections.OrderedDict([
                ('key5', 'value3'),
            ])),
        ])

        with io.StringIO() as stream:
            outputter = output.Stdout(file_=stream)
            outputter.output(data)
            result = stream.getvalue()

        expected = self.dedent_helper('''
            key1: value1

            key2:
              key3: value2

            key4:
              key5: value3
        ''')

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
