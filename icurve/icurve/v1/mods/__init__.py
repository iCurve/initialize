import importlib
import os
import inspect

from os import path
from types import FunctionType

from ..exceptions import DataNotFoundException
from ..service import DataService
from ..utils import enum, MARK_ENUM


class MODAPI(object):

    DAY = 86400
    WEEK = 604800
    MARK_ENUM = MARK_ENUM

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
        return self.data_service.get_line(start_time, end_time)

    def get_meta(self):
        return self.data_service.get_meta()


class ModManager(object):

    MOD_TYPE = enum(SINGLE=1, MULTI=0)
    MOD_METHOD = {
        # TODO: other mods...
        'sampling': MOD_TYPE.SINGLE,
        'reference': MOD_TYPE.MULTI,
        'make_band': MOD_TYPE.MULTI,
    }
    __ins = None
    mod_dir = path.abspath(path.join(path.dirname(inspect.getfile(inspect.currentframe())), '.'))
    mods = None

    def __init__(self, data):
        self.api = MODAPI(data)

    def __get_mods(self):
        if self.mods is None:
            self.mods = {}
            for mod in os.listdir(self.mod_dir):
                if path.exists(path.join(self.mod_dir, mod, "__init__.py")):
                    plugin = '.'.join(['icurve', 'v1', 'mods', mod])
                    mod = importlib.import_module(plugin)
                    self.mods[mod.__name__] = mod
        return self.mods

    def __call__(self, method, *args):
        res = []
        if method in self.MOD_METHOD:
            if self.MOD_METHOD[method] == self.MOD_TYPE.SINGLE:
                for mod_name, mod in sorted(self.__get_mods().items()):
                    if method in mod.__dict__ and isinstance(mod.__dict__[method], FunctionType):
                        return getattr(mod, method)(self.api, *args)
            else:
                for mod_name, mod in sorted(self.__get_mods().items()):
                    if method in mod.__dict__ and isinstance(mod.__dict__[method], FunctionType):
                        res.append(getattr(mod, method)(self.api, *args))
        return res

    def sampling(self, line, amount=1000):
        return self('sampling', line, amount)

    def make_band(self):
        return self('make_band')

    def reference(self, line):
        return self('reference', line)
