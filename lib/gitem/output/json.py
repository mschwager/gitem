#!/usr/bin/env python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import json

from . import base


class Json(base.Base):

    name = "json"

    def output(self, data):
        output = json.dumps(data, separators=(",", ":"))

        print(output, file=self.file)
