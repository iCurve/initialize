import urllib

from sqlalchemy.orm.exc import NoResultFound

from .utils import MARK_ENUM
from .exceptions import DataNotFoundException
from .models import Data, Point, db, Band


class DataMeta(object):
    def __init__(self, data):
        self.name = data.name
        self.start_time = data.start_time
        self.end_time = data.end_time
        self.period = data.period
        self.period_ratio = data.period_ratio
        self.label_ratio = data.label_ratio


class DataService(object):
    def __init__(self, data_name, meta=None, points=None):
        self.data_name = data_name
        self.cache = {}
        self.points = None
        if meta is not None and (isinstance(meta, DataMeta) or isinstance(meta, Data)):
            self.data = meta
        else:
            try:
                self.data = Data.query.filter_by(name=self.data_name).one()
            except NoResultFound:
                raise DataNotFoundException()
        if points is not None:
            self.points = points

    @staticmethod
    def list(pattern=None):
        if pattern:
            return Data.query.filter(db.text("name like :name")).params(name='%%%s%%' % pattern).order_by(Data.name).all()
        return Data.query.order_by(Data.name).all()

    def get_meta(self):
        return DataMeta(self.data)

    def get_data(self, start_time=None, end_time=None):
        if 'data' not in self.cache:
            if start_time is None or start_time < self.data.start_time:
                start_time = self.data.start_time
            if end_time is None or end_time > self.data.end_time:
                end_time = self.data.end_time
            if self.points is not None:
                points = [point for point in self.points if start_time <= point.timestamp <= end_time]
            else:
                points = Point.query.filter(db.and_(
                    Point.data_name.is_(self.data_name),
                    Point.timestamp.between(start_time, end_time)
                )).all()
                if start_time <= self.data.start_time and end_time >= self.data.end_time:
                    self.points = points
            line = [[point.timestamp, point.value, point.mark] for point in points]
            timestamps = {point.timestamp for point in points}
            for timestamp in range(start_time, end_time, self.data.period):
                if timestamp not in timestamps:
                    line.append([timestamp, None, None])
            self.cache['data'] = sorted(line)

        return self.cache['data']

    def get_line(self, start_time=None, end_time=None):
        if 'line' not in self.cache:
            if start_time is None or start_time < self.data.start_time:
                start_time = self.data.start_time
            if end_time is None or end_time > self.data.end_time:
                end_time = self.data.end_time
            if self.points is not None:
                points = [point for point in self.points if start_time <= point.timestamp <= end_time]
            else:
                points = Point.query.filter(db.and_(
                    Point.data_name.is_(self.data_name),
                    Point.timestamp.between(start_time, end_time)
                )).all()
                if start_time <= self.data.start_time and end_time >= self.data.end_time:
                    self.points = points
            line = [[point.timestamp, point.value] for point in points]
            timestamps = {point.timestamp for point in points}
            for timestamp in range(start_time, end_time, self.data.period):
                if timestamp not in timestamps:
                    line.append([timestamp, None])
            self.cache['line'] = sorted(line)

        return self.cache['line']

    def get_label(self, start_time=None, end_time=None):
        if 'label' not in self.cache:
            if start_time is None or start_time < self.data.start_time:
                start_time = self.data.start_time
            if end_time is None or end_time > self.data.end_time:
                end_time = self.data.end_time
            if self.points is not None:
                points = [point for point in self.points if start_time <= point.timestamp <= end_time]
            else:
                points = Point.query.filter(db.and_(
                    Point.data_name.is_(self.data_name),
                    Point.timestamp.between(start_time, end_time),
                    Point.mark.isnot(MARK_ENUM.normal)
                )).all()
                if start_time <= self.data.start_time and end_time >= self.data.end_time:
                    self.points = points
            line = [[point.timestamp, point.value] for point in points]
            timestamps = {point.timestamp for point in points}
            for timestamp in range(start_time, end_time, self.data.period):
                if timestamp not in timestamps:
                    line.append([timestamp, None])
            self.cache['label'] = sorted(line)

        return self.cache['label']

    def get_band(self, band_name, start_time=None, end_time=None, order=None):
        band_name = urllib.quote(band_name)
        query = Band.query.filter_by(data_name=self.data_name, name=band_name)
        if start_time is not None and end_time is not None:
            query = query.filter(db.or_(Band.start_time < end_time, Band.end_time > start_time))
        order = Band.start_time
        bands = query.order_by(order).all()
        bands = [{
            'bandNo': band_no + 1,
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
        if order == 'reliablity':
            bands = sorted(bands, key=lambda x: x['reliablity'])

        return bands

    def delete(self):
        Data.query.filter_by(name=self.data_name).delete(synchronize_session=False)
        Point.query.filter_by(data_name=self.data_name).delete(synchronize_session=False)
        Band.query.filter_by(data_name=self.data_name).delete(synchronize_session=False)
        db.session.commit()
