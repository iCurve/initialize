# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import csv

import time


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from flask import request, g
import urllib

from ..schemas import base_path
from . import Resource
from ..models import Data, Point, db, Band
from ..utils import str2time, parse_mark, MARK_ENUM, time2str
from ..service import DataService
from ..exceptions import DataNotFoundException
from ..mods import ModManager


class DataDataname(Resource):

    def get(self, dataName):
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name.encode('utf-8')
        try:
            string_io = StringIO()
            data = DataService(data_name).get_data()
            for key, point in enumerate(data):
                data[key][0] = time2str(data[key][0])
            csv.writer(string_io).writerows(data)

            return self.render_file('%s.csv' % data_name, string_io.getvalue())
        except DataNotFoundException:
            return self.render(msg='%s not found' % data_name), 404, None

    def post(self, dataName):
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name.encode('utf-8')
        try:
            DataService(data_name)
        except DataNotFoundException:
            for upload_file in request.files.values():
                line_no = 0
                points = []
                try:
                    reader = csv.reader(upload_file)
                    try:
                        line = reader.next()
                        if len(line) > 2:
                            points.append(Point(data_name, str2time(line[0]), float(line[1]), parse_mark(line[2])))
                        elif len(line) > 1:
                            points.append(Point(data_name, str2time(line[0]), float(line[1]), MARK_ENUM.normal))
                    except ValueError:
                        pass
                    for line in reader:
                        if len(line) > 2:
                            points.append(Point(data_name, str2time(line[0]), float(line[1]), parse_mark(line[2])))
                        elif len(line) > 1:
                            points.append(Point(data_name, str2time(line[0]), float(line[1]), MARK_ENUM.normal))
                except Exception as e:
                    return {'msg': 'line %d: %s' % (line_no, e.message), 'traceId': '', 'server': 'something'}, 422, {}
                if len(points) < 2:
                    return {'msg': 'at least 2 point', 'traceId': '', 'server': 'something'}, 422, {}
                # 清理旧数据
                Data.query.filter_by(name=data_name).delete(synchronize_session=False)
                Point.query.filter_by(data_name=data_name).delete(synchronize_session=False)
                for point in points:
                    db.session.add(point)
                timestamps = [point.timestamp for point in points]
                start_time = min(timestamps)
                end_time = max(timestamps)
                periods = []
                pre_timestamp = None
                for timestamp in timestamps:
                    if pre_timestamp is not None:
                        periods.append(timestamp - pre_timestamp)
                    pre_timestamp = timestamp
                sorted(periods)
                period = periods[len(periods) / 2]
                end_time += period
                period_ratio = sum([1 for x in periods if x == period]) * 1. / len(periods)
                label_ratio = sum([1 for point in points if point.mark]) * 1. / len(points)
                create_time = int(time.time())
                update_time = create_time
                data = Data(data_name, start_time, end_time, period, period_ratio, label_ratio, create_time, update_time)
                db.session.add(data)
                data_service = DataService(data_name, data, points)
                mod = ModManager(data_service)
                for band_name, bands in mod.make_band():
                    # TODO: sqlite3 中文
                    band_name = urllib.quote(band_name)
                    bands = [
                        Band(data_name, band_name, start_time, end_time, 0.5)
                        for start_time, end_time in bands
                    ]
                    for band in bands:
                        db.session.add(band)
                db.session.commit()

            return self.render(), 201, {'Location': '%s/data/%s' % (base_path, data_name)}
        else:
            return self.render(msg='%s is exists' % data_name), 422, None

    def put(self, dataName):
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name.encode('utf-8')
        # TODO: action
        print(g.form['startTime'])
        print(g.form['endTime'])
        print(g.form['action'])

        return self.render('Not Acceptable'), 405, None

    def delete(self, dataName):
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name.encode('utf-8')
        try:
            DataService(data_name).delete()
            return self.render(), 200, None
        except DataNotFoundException:
            return self.render(msg='%s not found' % data_name), 404, None
