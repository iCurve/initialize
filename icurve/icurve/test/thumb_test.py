# coding=utf-8
import uuid

from .base import IcurveTestCase

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class ThumbTestCase(IcurveTestCase):

    # TODO: 缩略图边界条件检查
    # 1. 抽样检查
    def test_thumb(self):
        # prepare
        data_name = str(uuid.uuid4()).replace('-', '')
        test_case = '20170828000000,52794.0,0\r\n' \
                    '20170828000100,52558.0,0\r\n' \
                    '20170828000200,51845.0,0\r\n' \
                    '20170828000300,51096.0,0\r\n' \
                    '20170828000400,51300.0,0\r\n' \
                    '20170828000500,50922.0,0\r\n' \
                    '20170828000600,50516.0,0\r\n' \
                    '20170828000700,50289.0,0\r\n' \
                    '20170828000800,49476.0,0\r\n' \
                    '20170828001000,49284.0,0\r\n' \
                    '20170828001100,49476.0,1\r\n'
        test_resp = {
            'type': 'line',
            'name': '抽样样例',
            'data': [
                [1503849600000, 52794.0],
                [1503849660000, 52558.0],
                [1503849720000, 51845.0],
                [1503849780000, 51096.0],
                [1503849840000, 51300.0],
                [1503849900000, 50922.0],
                [1503849960000, 50516.0],
                [1503850020000, 50289.0],
                [1503850080000, 49476.0],
                [1503850140000, None],
                [1503850200000, 49284.0],
                [1503850260000, 49476.0]
            ]
        }
        message = 'GET /v1/data/<dataName>/thumb 正常情况'
        self.client.post(path='/v1/data/%s' % data_name, data={'file': (StringIO(test_case), 'test.csv')})
        # test
        response = self.client.get(path='/v1/data/%s/thumb' % data_name)
        self.assertJsonResponse(response, 200, data=test_resp, message=message)
