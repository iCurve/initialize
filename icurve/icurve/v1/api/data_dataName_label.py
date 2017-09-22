# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import g

from ..service import DataService
from ..models import Point, db
from . import Resource
from .. import schemas


class DataDatanameLabel(Resource):

    def put(self, dataName):
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name = data_name.encode('utf-8')
        data_service = DataService(data_name)
        start_time = g.args['startTime'] / 1000
        end_time = g.args['endTime'] / 1000
        label = g.args['label']

        data_service.set_label(start_time, end_time, label)

        return self.render(), 200, None
