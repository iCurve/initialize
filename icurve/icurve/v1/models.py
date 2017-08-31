# coding=utf-8
from flask_sqlalchemy import SQLAlchemy

from .utils import repr_p

db = SQLAlchemy()


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    period_ratio = db.Column(db.Float, nullable=False)
    label_ratio = db.Column(db.Float, nullable=False)
    create_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer, nullable=False)

    def __init__(self, name, start_time, end_time, period, period_ratio, label_ratio, create_time, update_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.period_ratio = period_ratio
        self.label_ratio = label_ratio
        self.create_time = create_time
        self.update_time = update_time

    def __repr__(self):
        return repr_p(self)


class Point(db.Model):
    __tablename__ = 'point'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_name = db.Column(db.String(50), nullable=False)  # 外键？
    timestamp = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=True)
    mark = db.Column(db.Integer, nullable=False, default=-1)

    def __init__(self, data_name, timestamp, value, mark):
        self.data_name = data_name
        self.timestamp = timestamp
        self.value = value
        self.mark = mark

    def __repr__(self):
        return repr_p(self)


class Band(db.Model):
    __tablename__ = 'band'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_name = db.Column(db.String(50), nullable=False)  # 外键？
    name = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    reliablity = db.Column(db.Float, nullable=True)
