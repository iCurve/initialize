# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class DataDatanameCurves(Resource):

    def get(self, dataName):
        print(g.form)

        return {}, 200, None