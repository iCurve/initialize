# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from ..models import Band, db
from . import Resource
from .. import schemas


class DataDatanameBandBandname(Resource):
    def get(self, dataName, bandName):
        query = Band.query.filter_by(data_name=dataName, name=bandName)
        if 'startTime' in g.args and 'endTime' in g.args:
            start_time = g.args['startTime']
            end_time = g.args['endTime']
            query = query.filter(db.or_(Band.start_time < end_time, Band.end_time > start_time))
        order = Band.start_time
        bands = query.order_by(order).all()
        bands = [{
            'bandNo': band_no+1,
            'bandCount': len(bands),
            'currentTime': {
                'duration': {
                    'start': band.start_time * 1000,
                    'end': band.end_time * 1000
                },
                'show': {
                    'start': band.start_time - 600000,
                    'end': band.end_time + 600000
                },
            },
            'reliablity': band.reliablity
        } for band_no, band in enumerate(bands)]
        for band_no, band in enumerate(bands):
            if band_no - 1 > -1:
                bands[band_no - 1]['nextTime'] = band['currentTime']
            if band_no + 1 < len(bands):
                bands[band_no + 1]['preTime'] = band['currentTime']
        if 'order' in g.args:
            if g.args['order'] == 'reliablity':
                sorted(bands, key=lambda x: x['reliablity'])

        return self.render(data=bands), 200, None

    def delete(self, dataName, bandName):
        Band.query.filter_by(data_name=dataName, name=bandName).delete()
        return self.render(), 200, None
