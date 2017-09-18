# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import g

from ..service import DataService
from ..models import Band
from . import Resource
from .. import schemas


class DataDatanameBandBandname(Resource):
    def get(self, dataName, bandName):
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name.encode('utf-8')
        band_name = bandName
        if isinstance(bandName, unicode):
            band_name.encode('utf-8')
        data_service = DataService(data_name)
        # TODO: sqlite3 中文
        start_time = None
        end_time = None
        if 'startTime' in g.args:
            start_time = g.args['startTime']
        if 'endTime' in g.args:
            end_time = g.args['endTime']
        if start_time is not None and end_time is None:
            end_time = data_service.get_meta().end_time
        if end_time is not None and start_time is None:
            end_time = data_service.get_meta().start_time
        order = None
        if 'order' in g.args:
            order = g.args['order']

        bands = DataService(data_name).get_band(band_name.encode('utf-8'), start_time, end_time, order)

        return self.render(data=bands), 200, None

    def delete(self, dataName, bandName):
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name.encode('utf-8')
        band_name = bandName
        if isinstance(bandName, unicode):
            band_name.encode('utf-8')
        Band.query.filter_by(data_name=data_name, name=band_name).delete(synchronize_session=False)
        return self.render(), 200, None
