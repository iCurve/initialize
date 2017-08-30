# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class DataDatanameLabel(Resource):

    def put(self, dataName):
        print(g.form)

        return {'msg': 'something', 'traceId': 'something', 'server': 'something'}, 200, None