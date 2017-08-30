# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class DataDatanameBandBandname(Resource):

    def get(self, dataName, bandName):
        print(g.args)
        print(g.form)

        return {}, 200, None

    def delete(self, dataName, bandName):

        return {'msg': 'something', 'traceId': 'something', 'server': 'something'}, 200, None