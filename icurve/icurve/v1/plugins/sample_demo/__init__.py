# coding=utf-8
import math


def sampling(api, line, amount):
    """
    抽样样例
    :param api: 可调用的 api
    :param line: 曲线 [(timestamp, value...)]
    :param amount: 抽样后的点数
    :return: [(timestamp, value...)]
    """
    if amount < 1 or len(line) < amount:
        return '抽样样例', line
    period = api.get_meta().period
    start_time = line[0][0]
    end_time = line[-1][0] + period
    sample_period = floor((end_time - start_time + .0) / amount, period)
    tmp_value = {
        timestamp: []
        for timestamp in range(
            start_time / sample_period * sample_period,
            end_time,
            sample_period
        )
    }
    for point in line:
        tmp_value[point[0] / sample_period * sample_period].append(point[1:])
    result = []
    for timestamp in sorted(tmp_value.keys()):
        value = [x[0] for x in tmp_value[timestamp] if x[0] is not None]
        if len(value) > 0:
            value = float(sum(value)/len(value))
        else:
            value = None
        label = [x[1] for x in tmp_value[timestamp] if len(x) > 1 and x[1] is not None]
        if len(label) > 0:
            label = max(label)
        else:
            label = api.LABEL_ENUM.normal
        result.append([timestamp, value, label])

    return '抽样样例', result


def floor(data, base=None):
    if base is None or base == 0:
        return math.floor(data)
    return int(math.floor(data / base) * base)


def ceil(data, base=None):
    if base is None or base == 0:
        return math.floor(data)
    return int(math.ceil(data / base) * base)
