# coding=utf-8


def reference(api, line):
    """
    参考线样例，触发条件为趋势图加载
    :param api: 可调用的 api
    :param line: 局部原始数据 [(timestamp, value...)]
    :return: [(timestamp, value)]
    """
    result = []

    if len(line) > 0:
        start_time = line[0][0]
        end_time = line[-1][0]
        result.append(api.get_data(start_time - api.DAY, end_time - api.DAY))

    return '天同比', result