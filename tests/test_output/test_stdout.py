#!/usr/bin/env python

import io
import textwrap
import unittest

from gitem import output


class TestStdout(unittest.TestCase):

    @staticmethod
    def dedent_helper(s):
        return textwrap.dedent(s).lstrip()

    def test_basic(self):
        with io.StringIO() as stream:
            outputter = output.Stdout(file_=stream)
            outputter.output('key', 'value')
            result = stream.getvalue()

        expected = self.dedent_helper('''
            key: value
        ''')

        self.assertEqual(result, expected)

    def test_depth(self):
        with io.StringIO() as stream:
            outputter = output.Stdout(file_=stream)
            outputter.output('key1', 'value1')
            outputter.output('key2', 'value2', depth=2)
            result = stream.getvalue()

        expected = self.dedent_helper('''
            key1: value1
              key2: value2
        ''')

        self.assertEqual(result, expected)

    def test_just_key(self):
        with io.StringIO() as stream:
            outputter = output.Stdout(file_=stream)
            outputter.output('key')
            result = stream.getvalue()

        expected = self.dedent_helper('''
            key:
        ''')

        self.assertEqual(result, expected)

    def test_no_key(self):
        with io.StringIO() as stream:
            outputter = output.Stdout(file_=stream)
            outputter.output('')
            result = stream.getvalue()

        expected = '\n'

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
