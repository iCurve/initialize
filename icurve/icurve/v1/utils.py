# coding=utf-8
import time
import math


def enum(**enums):
    return type('Enum', (), enums)


LABEL_ENUM = enum(normal=0, abnormal=1, unknown=-1)
REPR_FILTER = {'_sa_instance_state'}
DEFAULT_TIMEFORMAT = '%Y%m%d%H%M%S'


def time2str(time_unix):
    return time.strftime(DEFAULT_TIMEFORMAT, time.localtime(time_unix))


def str2time(time_str):
    if len(time_str) == 14:  # 可读秒级时间戳
        return int(time.mktime(time.strptime(time_str, DEFAULT_TIMEFORMAT)))
    # 默认使用 unix 时间戳
    return int(time_str)


def parse_label(label_str):
    label = int(label_str)
    if label not in {LABEL_ENUM.normal, LABEL_ENUM.abnormal}:
        raise Exception('label %s not valid.' % label_str)
    return label


def repr_p(obj):
    return '<%s %s>' % (obj.__class__.__name__, ' '.join(['%s:%s' % item for item in obj.__dict__.items() if item[0] not
                                                          in REPR_FILTER]))


def s2ms(data):
    res = []
    for point in data:
        point = list(point)
        point[0] *= 1000
        res.append(point)
    return res


def floor(data, base=None):
    if base is None or base == 0:
        return math.floor(data)
    return int(math.floor(data / base) * base)


def ceil(data, base=None):
    if base is None or base == 0:
        return math.floor(data)
    return int(math.ceil(data / base) * base)
