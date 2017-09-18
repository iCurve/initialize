# coding=utf-8
import time


def enum(**enums):
    return type('Enum', (), enums)


MARK_ENUM = enum(normal=0, abnormal=1, unknown=-1)
REPR_FILTER = {'_sa_instance_state'}
DEFAULT_TIMEFORMAT = '%Y%m%d%H%M%S'


def time2str(time_unix):
    return time.strftime(DEFAULT_TIMEFORMAT, time.localtime(time_unix))


def str2time(time_str):
    if len(time_str) == 14:  # 可读秒级时间戳
        return int(time.mktime(time.strptime(time_str, DEFAULT_TIMEFORMAT)))
    # 默认使用 unix 时间戳
    return int(time_str)


def parse_mark(mark_str):
    mark = int(mark_str)
    if mark not in {MARK_ENUM.normal, MARK_ENUM.abnormal}:
        raise Exception('mark %s not valid.' % mark_str)
    return mark


def repr_p(obj):
    return '<%s %s>' % (obj.__class__.__name__, ' '.join(['%s:%s' % item for item in obj.__dict__.items() if item[0] not
                                                          in REPR_FILTER]))


def s2ms(data):
    for key, point in enumerate(data):
        data[key][0] *= 1000
    return data
