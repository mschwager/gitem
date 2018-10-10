#!/usr/bin/env python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import abc
import sys


class Base(abc.ABC):

    name = "base"

    def __init__(self, file_=sys.stdout):
        self.file = file_

    @abc.abstractmethod
    def output(self):
        pass
