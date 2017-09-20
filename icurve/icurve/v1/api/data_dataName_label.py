# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import g

from ..service import DataService
from ..models import Point, db
from . import Resource
from .. import schemas


class DataDatanameLabel(Resource):

    def put(self, dataName):
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name = data_name.encode('utf-8')
        data_service = DataService(data_name)

        Point.query.filter(db.and_(
            Point.data_name.is_(data_name),
            Point.timestamp.between(g.args['startTime'] / 1000, g.args['endTime'] / 1000)
        )).update({Point.mark: g.args['label']}, synchronize_session=False)
        db.session.commit()

        return self.render(), 200, None
