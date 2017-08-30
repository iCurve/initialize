# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import copy
import random

from flask import request, g

from ..models import Data, Point, db
from . import Resource
from .. import schemas


class DataDatanameCurves(Resource):

    def get(self, dataName):
        lines = []
        data = Data.query.filter_by(name=dataName).one()
        start_time = max(g.args['startTime'], data.start_time)
        end_time = min(g.args['endTime'], data.end_time)
        period = data.period
        points = Point.query.filter(db.and_(
            Point.data_name.is_(dataName),
            Point.timestamp.between(start_time, end_time)
        )).all()
        line = {timestamp: None for timestamp in range(start_time, end_time + period, period)}
        for point in points:
            key = point.timestamp / period * period
            if line[key] is None:
                line[key] = 0
            line[key] += point.value
        line = sorted([(timestamp, value) for timestamp, value in line.items()])
        label = {timestamp: None for timestamp in range(start_time, end_time, period)}
        for point in points:
            if point.mark != 1:
                continue
            key = point.timestamp / period * period
            if label[key] is None:
                label[key] = 0
            label[key] += point.value
        label = sorted([(timestamp, value) for timestamp, value in label.items()])

        # TODO: 参考线等
        refs = []
        for point in line:
            if point[1] is not None:
                refs.append((point[0], point[1] + int(random.gauss(20, 10000))))
            else:
                refs.append(point)
        lines.append({
            'name': '周同比',
            'type': 'line',
            'data': refs
        })
        refs = []
        for point in line:
            if point[1] is not None:
                refs.append((point[0], point[1] + int(random.gauss(5, 100))))
            else:
                refs.append(point)
        lines.append({
            'name': '天同比',
            'type': 'line',
            'data': refs
        })
        refs = []
        for point in line:
            if point[1] is not None:
                refs.append((point[0], point[1] - int(random.gauss(5, 1000)), point[1] + int(random.gauss(5, 1000))))
            else:
                refs.append(point)
        lines.append({
            'name': '参考区间',
            'type': 'arearange',
            'data': refs
        })

        # 原始曲线
        lines.append({
            'name': '原始曲线',
            'type': 'line',
            'data': line
        })
        # 标注曲线
        lines.append({
            'name': '标注曲线',
            'type': 'line',
            'data': label
        })

        return {
           'data': lines,
           'msg': 'OK',
           'traceId': '',
           'server': ''
        }, 200, None