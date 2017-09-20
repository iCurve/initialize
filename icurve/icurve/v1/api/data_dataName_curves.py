# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import urllib
from operator import itemgetter

from flask import g

from ..utils import s2ms
from ..plugins import PluginManager
from ..service import DataService
from ..models import db, Band
from . import Resource
from .. import schemas


class DataDatanameCurves(Resource):

    def get(self, dataName):
        trends = []
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name = data_name.encode('utf-8')
        data_service = DataService(data_name)
        plugin = PluginManager(data_service)
        start_time = g.args['startTime'] / 1000
        end_time = g.args['endTime'] / 1000

        line = data_service.get_data(start_time, end_time)
        _, line = plugin.sampling(line)

        y_axis = [float('inf'), float('-inf')]

        values = [point[1] for point in line if point[1] is not None]
        if len(values) > 0:
            y_axis[1] = max(y_axis[1], max(values))
            y_axis[0] = min(y_axis[1], min(values))

        refs = plugin.reference(line)

        for ref_name, ref in refs:
            if len(ref) > 0 and len(ref[0]) == 2:
                ref_type = 'line'
                values = [point[1] for point in ref if point[1] is not None]
            elif len(ref) > 0 and len(ref[0]) == 3:
                ref_type = 'arearange'
                values = [point[1] for point in ref if point[1] is not None] + \
                         [point[2] for point in ref if point[2] is not None]
            else:
                continue
            if len(values) > 0:
                y_axis[1] = max(y_axis[1], max(values))
                y_axis[0] = min(y_axis[0], min(values))
            trends.append({
                'name': ref_name,
                'type': ref_type,
                'data': ref
            })

        # TODO: yAxis
        if y_axis[1] == float('-inf'):
            y_axis[1] = 0
        if y_axis[0] == float('inf'):
            y_axis[0] = 0
        length = y_axis[1] - y_axis[0]
        if y_axis[1] != 100:
            y_axis[1] += 0.1 * length
        if y_axis[0] != 0:
            y_axis[0] -= 0.1 * length

        # 原始曲线
        trends.append({
            'name': '原始曲线',
            'type': 'line',
            'data': s2ms(line)
        })
        # 标注曲线
        trends.append({
            'name': '标注曲线',
            'type': 'line',
            'data': s2ms(line)
        })

        bands = []
        band_names = db.session.query(db.distinct(Band.name)).all()
        for band_name, in band_names:
            # 色块渲染
            band_name = urllib.unquote(band_name.encode('utf-8'))
            band_items = data_service.get_band(band_name, start_time, end_time)
            line = []
            for band_item in band_items:
                for x in range(band_item[0], band_item[1], data_service.get_meta().period):
                    line.append([x, y_axis[1]])
            trends.append({
                'name': band_name,
                'type': 'area',
                'data': s2ms(line)
            })

            # band tool 渲染
            band_items = [{
                'bandNo': band_no + 1,
                'bandCount': len(band_items),
                'currentTime': {
                    'duration': {
                        'start': band[0] * 1000,
                        'end': band[1] * 1000
                    },
                    'show': {
                        'start': (band[0] - (start_time - end_time) / 2) * 1000,
                        'end': (band[1] + (start_time - end_time) / 2) * 1000
                    },
                },
                'reliablity': band[2]
            } for band_no, band in enumerate(band_items)]
            for band_no, band in enumerate(band_items):
                if band_no - 1 > -1:
                    band_items[band_no - 1]['nextTime'] = band['currentTime']['show']
                if band_no + 1 < len(band_items):
                    band_items[band_no + 1]['preTime'] = band['currentTime']['show']

            bands.append({
                'name': band_name,
                'bands': band_items
            })

        return self.render(data={
            'trends': trends,
            'bands': bands,
            'yAxis': y_axis
        }), 200, None
