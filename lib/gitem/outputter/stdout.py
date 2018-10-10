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

    def output(self, key, value="", depth=0):
        if value:
            output = "{}: {}".format(key, value)
        else:
            output = "{}:".format(key)

        print(" " * depth + output, file=self.file)
