# coding=utf-8
def make_band(api):
    line = api.get_data()
    abnormal_bands = []
    for point_no, point in enumerate(sorted(line)[6:]):
        if point[1] > sum([x[1] for x in line[point_no - 6:point_no - 1] if x[1] is not None]) * 0.21:
            if not abnormal_bands or len(abnormal_bands[-1]) == 2:
                abnormal_bands.append([point[0]])
        elif len(abnormal_bands[-1]) == 1:
            abnormal_bands[-1].append(point[0])
    if len(abnormal_bands[-1]) == 1:
        abnormal_bands[-1].append(sorted(line)[-1][0])

    return '5min滑动窗口 环比上涨5%', abnormal_bands
