# coding=utf-8
import importlib
import os
import inspect

from os import path
from types import FunctionType

from flask import current_app

from ..exceptions import DataNotFoundException
from ..service import DataService
from ..utils import enum, LABEL_ENUM


class API(object):

    DAY = 86400
    WEEK = 604800
    LABEL_ENUM = LABEL_ENUM

    def __init__(self, data):
        if isinstance(data, str):
            self.data_name = data
            self.data_service = DataService(data)
        elif isinstance(data, DataService):
            self.data_name = data.get_meta().name
            self.data_service = data
        else:
            raise DataNotFoundException

    def get_data(self, start_time=None, end_time=None):
        """
        获取数据
        :param start_time: 开始时间
        :param end_time: 结束时间
        :return: [(timestamp, value, label)]
        """
        return self.data_service.get_line(start_time, end_time)

    def get_meta(self):
        """
        获取 meta 信息
        :return: Meta(name, start_time, end_time, period)
        """
        return self.data_service.get_meta()

    def set_label(self, start_time, end_time, label):
        """
        设置 label
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param label: label 内容 MARK_ENUM.normal MARK_ENUM.abnormal
        :return:
        """
        return self.data_service.set_label(start_time, end_time, label)

    def set_band(self, band_name, start_time, end_time, reliablity):
        """
        添加 band
        :param band_name: band 名称
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param reliablity: 置信度
        :return:
        """
        return self.data_service.set_band(band_name, start_time, end_time, reliablity)


class PluginManager(object):

    PLUGIN_TYPE = enum(SINGLE=1, MULTI=0)
    PLUGIN_METHOD = {
        # TODO: other plugins...
        'sampling': PLUGIN_TYPE.SINGLE,
        'reference': PLUGIN_TYPE.MULTI,
        'init_band': PLUGIN_TYPE.MULTI,
    }
    __ins = None
    plugin_dir = path.abspath(path.join(path.dirname(inspect.getfile(inspect.currentframe())), '.'))
    plugins = None
    menus = None

    def __init__(self, data):
        self.api = API(data)

    @staticmethod
    def __get_plugins():
        if PluginManager.plugins is None:
            PluginManager.plugins = {}
            for plugin in os.listdir(PluginManager.plugin_dir):
                if path.exists(path.join(PluginManager.plugin_dir, plugin, "__init__.py")):
                    plugin_path = '.'.join([current_app.root_path.split(os.sep)[-1], 'v1', 'plugins', plugin])
                    plugin = importlib.import_module(plugin_path)
                    PluginManager.plugins[plugin.__name__] = plugin
        return PluginManager.plugins

    def __call__(self, method, *args):
        res = []
        if method in self.PLUGIN_METHOD:
            if self.PLUGIN_METHOD[method] == self.PLUGIN_TYPE.SINGLE:
                for _, plugin in sorted(PluginManager.__get_plugins().items()):
                    if method in plugin.__dict__ and isinstance(plugin.__dict__[method], FunctionType):
                        return getattr(plugin, method)(self.api, *args)
            else:
                for _, plugin in sorted(PluginManager.__get_plugins().items()):
                    if method in plugin.__dict__ and isinstance(plugin.__dict__[method], FunctionType):
                        output = getattr(plugin, method)(self.api, *args)
                        if output is not None:
                            res.append(output)
        return res

    def sampling(self, line, amount=1000):
        return self('sampling', line, amount)

    def init_band(self):
        return self('init_band')

    def reference(self, line):
        return self('reference', line)

    @staticmethod
    def get_menus():
        if PluginManager.menus is None:
            PluginManager.menus = []
            method = 'menus'
            for _, plugin in sorted(PluginManager.__get_plugins().items()):
                if method in plugin.__dict__ and isinstance(plugin.__dict__[method], FunctionType):
                    output = getattr(plugin, method)()
                    if output is not None:
                        PluginManager.menus.extend(output)
        return PluginManager.menus
