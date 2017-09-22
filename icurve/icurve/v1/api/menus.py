# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from ..plugins import PluginManager
from . import Resource
from .. import schemas


class Menus(Resource):

    def get(self):
        actions = [
            {
                "action": menu[0],
                "name": menu[1]
            }
            for menu in PluginManager.get_menus()
        ]
        return self.render(data=actions), 200, None
