# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from ..plugins import PluginManager
from ..service import DataService
from ..utils import s2ms
from . import Resource
from .. import schemas


class DataDatanameThumb(Resource):

    def get(self, dataName):
        data_name = dataName
        if isinstance(data_name, unicode):
            data_name = data_name.encode('utf-8')
        data_service = DataService(data_name)
        plugin = PluginManager(data_name)
        line = data_service.get_line()

        thumb_name, thumb = plugin.sampling(line, 1440)

        return self.render(data={
                'name': thumb_name,
                'type': 'line',
                'data': s2ms(thumb)
            }), 200, None
