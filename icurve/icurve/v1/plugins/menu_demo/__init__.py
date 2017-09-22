# coding=utf-8


def menus():
    """
    菜单项
    :return: [(action, menu_name)]
    """
    return [
        ('cancel_label', '取消标注')
    ]


def cancel_label(api, start_time, end_time):
    """
    菜单项操作
    :func action: action in menus
    :param api: 可调用 api
    :param start_time: 开始时间
    :param end_time: 结束时间
    :return: 给前端的返回
    """
    api.set_label(start_time, end_time, api.LABEL_ENUM.normal)
    return ''
