# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from ..models import Point, db
from . import Resource
from .. import schemas


class DataDatanameLabel(Resource):

    def put(self, dataName):
        Point.query.filter(db.and_(
            Point.data_name.is_(dataName),
            Point.timestamp.between(g.args['startTime'], g.args['endTime'])
        )).update({Point.mark: g.args['label']}, synchronize_session=False)
        db.session.commit()

        return self.render(), 200, None
