# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import urllib
from operator import itemgetter

from flask import g

from utils import s2ms
from ..mods import ModManager
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
        mod = ModManager(data_service)
        start_time = g.args['startTime']
        end_time = g.args['endTime']

        line = data_service.get_data(start_time, end_time)
        _, line = mod.sampling(line)

        y_axis = [float('inf'), float('-inf')]
        y_axis[1] = max(y_axis[1], max(line, key=itemgetter(1)))
        y_axis[0] = min(y_axis[0], min(line, key=itemgetter(1)))

        refs = mod.reference(line)

        for ref_name, ref in refs:
            if len(ref[0]) == 2:
                ref_type = 'line'
                y_axis[1] = max(y_axis[1], max(ref, key=itemgetter(1)))
                y_axis[0] = min(y_axis[0], min(ref, key=itemgetter(1)))
            elif len(ref[0]) == 3:
                ref_type = 'arearange'
                y_axis[1] = max(y_axis[1], max(ref, key=itemgetter(2)))
                y_axis[0] = min(y_axis[0], min(ref, key=itemgetter(1)))
            else:
                continue
            trends.append({
                'name': ref_name,
                'type': ref_type,
                'data': ref
            })

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
