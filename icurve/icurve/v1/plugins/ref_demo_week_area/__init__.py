# coding=utf-8
def reference(api, line):
    """
    参考区域样例，触发条件为趋势图加载
    :param api: 可调用的 api
    :param line: 局部原始数据 [(timestamp, value...)]
    :return: [(timestamp, y_lower, y_upper)]
    """
    result = []

    if len(line) > 0:
        start_time = line[0][0]
        end_time = line[-1][0]

        line = api.get_data(start_time - api.WEEK, end_time - api.WEEK)
        area = [
            # (timestamp, lower, upper)
            (timestamp, value*0.9, value*1.1)
            for timestamp, value in line
        ]
        result.append(area)

    return '周同比10%', result