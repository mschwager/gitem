#!/usr/bin/env python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from . import base


class Stdout(base.Base):

    name = "stdout"
    depth_increment = 2

    def __init__(self, *args, **kwargs):
        self.first_recurse = True

        super(Stdout, self).__init__(*args, **kwargs)

    def output_helper(self, data, depth):
        for i, (key, value) in enumerate(data.items()):
            if isinstance(value, dict):
                if depth == 0 and i == 0 and self.first_recurse:
                    # If we're on the very first dict then don't include an
                    # awkward newline before we've printed anything else
                    self.first_recurse = False
                else:
                    print("", file=self.file)

                output = "{}:".format(key)
                print(" " * depth + output, file=self.file)

                self.output_helper(value, depth + self.depth_increment)
            elif isinstance(value, list):
                output = "{}:".format(key)
                print(" " * depth + output, file=self.file)

                for l in value:
                    print(" " * (depth + self.depth_increment) + l, file=self.file)
            else:
                if value == "":
                    output = "{}:".format(key)
                else:
                    output = "{}: {}".format(key, value)

                print(" " * depth + output, file=self.file)

    def output(self, data):
        self.output_helper(data, 0)
