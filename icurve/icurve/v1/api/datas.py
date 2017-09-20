# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import g

from ..service import DataService
from . import Resource
from .. import schemas


class Datas(Resource):

    def get(self):
        pattern = None
        if 'pattern' in g.args:
            pattern = g.args['pattern']
        datas = DataService.list(pattern)

        datas = [
            {
                "id": data.id,
                "name": data.name,
                "uri": '/v1/data/%s' % data.name,
                "createTime": data.create_time * 1000,
                "updateTime": data.update_time * 1000,
                "labelRatio": data.label_ratio,
                "period": {
                    "length": data.period,
                    "ratio": data.period_ratio
                },
                "time": {
                    "start": data.start_time * 1000,
                    "end": data.end_time * 1000
                }
            } for data in datas
        ]

        return self.render(data=datas), 200, None
