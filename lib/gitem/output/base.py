#!/usr/bin/env python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import abc
import sys

if sys.version_info >= (3, 4):
    ABC = abc.ABC
else:
    ABC = abc.ABCMeta(str('ABC'), (), {})


class Base(ABC):

    name = "base"

    def __init__(self, file_=sys.stdout):
        self.file = file_

    @abc.abstractmethod
    def output(self):
        pass
