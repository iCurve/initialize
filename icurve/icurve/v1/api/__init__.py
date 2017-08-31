# -*- coding: utf-8 -*-
from __future__ import absolute_import

import flask_restful as restful
from flask import request

from ..validators import request_validate, response_filter


class Resource(restful.Resource):
    method_decorators = [request_validate, response_filter]

    @staticmethod
    def render(msg='OK', data=None):
        host = request.host
        if ':' in host:
            host = host.split(':')[0]
        resp = {
            'msg': msg,
            'traceId': '',
            'server': host
        }
        if data is not None:
            resp['data'] = data
        return resp
