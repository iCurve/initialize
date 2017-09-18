# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import urllib

from flask import g

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

        refs = mod.reference(line)

        for ref in refs:
            if len(ref) < 2 or len(ref[1]) < 1:
                continue
            if len(ref[1][0]) == 2:
                ref_type = 'line'
            elif len(ref[1][0]) == 3:
                ref_type = 'arearange'
            else:
                continue
            trends.append({
                'name': ref[0],
                'type': ref_type,
                'data': ref[1]
            })

        # 原始曲线
        trends.append({
            'name': '原始曲线',
            'type': 'line',
            'data': line
        })
        # 标注曲线
        trends.append({
            'name': '标注曲线',
            'type': 'line',
            'data': line
        })

        bands = []
        band_names = db.session.query(db.distinct(Band.name)).all()
        for band_name, in band_names:
            bands.append({
                'name': urllib.unquote(band_name.encode('utf-8')),
                'bands': data_service.get_band(urllib.unquote(band_name.encode('utf-8')), start_time, end_time)
            })
        return self.render(data={
            'trends': trends,
            'bands': bands
        }), 200, None
