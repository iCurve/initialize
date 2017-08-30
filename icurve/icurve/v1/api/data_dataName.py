# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import csv
import os

import time

import StringIO
from flask import request, g, current_app, make_response

from . import Resource
from ..models import Data, Point, db
from ..utils import str2time, parse_mark, time2str
from .. import schemas


class DataDataname(Resource):

    def get(self, dataName):
        string_io = StringIO.StringIO()
        writer = csv.writer(string_io)
        for point in Point.query.filter_by(data_name=dataName).all():
            writer.writerow([time2str(point.timestamp), point.value, point.mark])
        return current_app.response_class(
            string_io.getvalue(),
            status=200,
            headers={'Content-Disposition': 'attachment; filename=%s.csv' % dataName},
            mimetype='application/json'
        )

    def post(self, dataName):
        for upload_file in request.files.values():
            line_no = 0
            point_list = []
            try:
                for line_no, line in enumerate(csv.reader(upload_file)):
                    # TODO: 首行错误格式处理
                    point_list.append(Point(dataName, str2time(line[0]), float(line[1]), parse_mark(line[2])))
            except Exception as e:
                return {'msg': 'line %d: %s' % (line_no, e.message), 'traceId': '', 'server': 'something'}, 422, {}
            if len(point_list) < 2:
                return {'msg': 'at least 2 point', 'traceId': '', 'server': 'something'}, 422, {}
            # 清理旧数据
            Data.query.filter_by(name=dataName).delete()
            Point.query.filter_by(data_name=dataName).delete()
            for point in point_list:
                db.session.add(point)
            timestamps = [point.timestamp for point in point_list]
            start_time = min(timestamps)
            end_time = max(timestamps)
            periods = []
            pre_timestamp = None
            for timestamp in timestamps:
                if pre_timestamp is not None:
                    periods.append(timestamp - pre_timestamp)
                pre_timestamp = timestamp
            sorted(periods)
            period = periods[len(periods)/2]
            period_ratio = sum([1 for x in periods if x == period]) * 1. / len(periods)
            label_ratio = sum([1 for point in point_list if point.mark]) * 1. / len(point_list)
            create_time = int(time.time())
            update_time = create_time
            data = Data(dataName, start_time, end_time,period, period_ratio, label_ratio, create_time, update_time)
            db.session.add(data)
            db.session.commit()

        return {'msg': 'OK', 'traceId': '', 'server': ''}, 201, {'Location': '/data/%s' % dataName}

    def put(self, dataName):
        print(g.form)

        return {'msg': 'something', 'traceId': 'something', 'server': 'something'}, 200, None

    def delete(self, dataName):

        return {'msg': 'something', 'traceId': 'something', 'server': 'something'}, 405, None
