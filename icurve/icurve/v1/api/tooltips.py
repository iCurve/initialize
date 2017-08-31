# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class Tooltips(Resource):

    def get(self):
        actions = [{
            "action": "foo",
            "name": "占位操作"
        }]
        return self.render(data=actions), 200, None
