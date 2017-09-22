# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import urllib

from flask import g

from ..exceptions import DataNotFoundException
from ..utils import s2ms, LABEL_ENUM
from ..plugins import PluginManager
from ..service import DataService
from ..models import db, Band
from . import Resource
from .. import schemas


class DataDatanameCurves(Resource):

    def get(self, dataName):
        # 参数解析
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name = data_name.encode('utf-8')
        try:
            data_service = DataService(data_name)
        except DataNotFoundException:
            return self.render(msg='%s not found' % data_name), 404, None
        plugin = PluginManager(data_service)
        start_time = g.args['startTime'] / 1000
        end_time = g.args['endTime'] / 1000
        period = data_service.get_meta().period

        # 原始数据获取
        line = data_service.get_data(start_time, end_time)

        # 原始数据计算
        raw_line = [point[:2] for point in line]
        _, raw_line = plugin.sampling(raw_line)
        raw_line = s2ms(raw_line)

        raw_line = {
            'name': '原始曲线',
            'type': 'line',
            'data': raw_line
        }

        # 标注曲线计算
        label_line = [(point[0], point[2]) for point in line]
        _, label_line = plugin.sampling(label_line)
        for key, point in enumerate(label_line):
            if point[1] == LABEL_ENUM.abnormal:
                label_line[key] = raw_line['data'][key]
            else:
                label_line[key] = (raw_line['data'][key][0], None)
        label_line = {
            'name': '标注曲线',
            'type': 'line',
            'data': label_line
        }

        y_axis = [float('inf'), float('-inf')]

        # y 轴计算
        values = [point[1] for point in line if point[1] is not None]
        if len(values) > 0:
            y_axis[1] = max(y_axis[1], max(values))
            y_axis[0] = min(y_axis[1], min(values))

        # 参考线计算
        refs = plugin.reference(line)
        ref_lines = []
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
            ref_lines.append({
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

        bands = []
        band_lines = []
        band_names = db.session.query(db.distinct(Band.name)).all()
        for band_name, in band_names:
            # 色块渲染
            band_name = urllib.unquote(band_name.encode('utf-8'))
            band_items = data_service.get_band(band_name, start_time, end_time)
            tmp = set([])
            for band_item in band_items:
                for x in range(band_item[0], band_item[1] + period, period):
                    tmp.add(x)
            band_line = []
            for point in line:
                if point[0] in tmp:
                    band_line.append([point[0], y_axis[1]])
                else:
                    band_line.append([point[0], None])
            band_lines.append({
                'name': band_name,
                'type': 'area',
                'data': s2ms(band_line)
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

        # trend 拼装
        trends = ref_lines + [raw_line] + [label_line] + band_lines

        return self.render(data={
            'trends': trends,
            'bands': bands,
            'yAxis': y_axis
        }), 200, None
