# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
from math import ceil

from ..models import Point, Data
from . import Resource
from .. import schemas


class DataDatanameThumb(Resource):

    def get(self, dataName):
        amount = 500
        data = Data.query.filter_by(name=dataName).one()
        points = Point.query.filter_by(data_name=dataName).all()
        start_time = data.start_time
        end_time = data.end_time
        period = int(ceil((end_time - start_time + .0) / amount / data.period)) * data.period
        data = {timestamp: None for timestamp in range(start_time, end_time, period)}
        for point in points:
            key = point.timestamp / period * period
            # debug
            if key not in data:
                print(key)
            if data[key] is None:
                data[key] = 0
            data[key] += point.value

        return self.render(data={
                'name': 'thumb',
                'type': 'line',
                'data': sorted([(timestamp * 1000, value) for timestamp, value in data.items()])
            }), 200, None
