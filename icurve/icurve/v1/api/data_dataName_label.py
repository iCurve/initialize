# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from ..utils import MARK_ENUM, parse_mark
from ..models import Point, db
from . import Resource
from .. import schemas


class DataDatanameLabel(Resource):

    def put(self, dataName):
        Point.query.filter(db.and_(
            Point.data_name.is_(dataName),
            Point.timestamp.between(g.form['startTime'], g.form['endTime'])
        )).update({Point.mark: g.form['label']}, synchronize_session=False)
        db.session.commit()

        return {'msg': 'OK', 'traceId': '', 'server': ''}, 200, None
