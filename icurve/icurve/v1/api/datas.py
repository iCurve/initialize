# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from ..models import db, Data
from . import Resource
from .. import schemas


class Datas(Resource):

    def get(self):
        query = Data.query
        if 'pattern' in g.args:
            query = query.filter(db.text("name like :name")).params(name='%%%s%%' % g.args['pattern'])
        data = query.order_by(Data.name).all()
        for index, value in enumerate(data):
            # 数据重新装箱
            data[index] = {
                "id": value.id,
                "name": value.name,
                "uri": '/v1/data/%s' % value.name,
                "createTime": value.create_time * 1000,
                "updateTime": value.update_time * 1000,
                "labelRatio": value.label_ratio,
                "period": {
                    "length": value.period,
                    "ratio": value.period_ratio
                },
                "time": {
                    "start": value.start_time * 1000,
                    "end": value.end_time * 1000
                }
            }

        return self.render(data=data), 200, None
