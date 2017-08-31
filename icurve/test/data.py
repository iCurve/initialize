# coding=utf-8
import uuid

from .base_test_case import IcurveTestCase

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class DataTestCase(IcurveTestCase):

    data_names = []

    # TODO: 加载数据异常边界的检查
    # 1. 特殊文件名
    # 2. 非法 csv
    # 3. 带表头的 csv
    # 4. timestamp, value, mark 边界条件
    def test_post_data(self):
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
        message = 'POST /v1/data/<dataName> 正常情况'
        # test
        response = self.client.post(path='/v1/data/%s' % data_name, data={'file': (StringIO(test_case), 'test.csv')})
        self.assertJsonResponse(
            response,
            201,
            {'Location': 'http://localhost/v1/data/%s' % data_name},
            None,
            message
        )

    # TODO: 下载数据异常边界的检查
    # 1. 特殊文件名
    def test_get_data(self):
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
        test_resp = test_case
        test_header = {
            'Content-Type': 'application/json',
            'Content-Disposition': 'attachment; filename=%s.csv' % data_name
        }
        message = 'GET /v1/data/<dataName> 正常情况'
        self.client.post(path='/v1/data/%s' % data_name, data={'file': (StringIO(test_case), 'test.csv')})
        # test
        response = self.client.get(path='/v1/data/%s' % data_name)
        self.assertEqual(response.status_code, 200)
        resp_headers = {key: value for key, value in response.headers}
        for key, value in test_header.items():
            self.assertIn(key, resp_headers, message)
            self.assertEqual(value, resp_headers[key], message)
        self.assertEqual(response.data, test_resp)

    # TODO: 删除效果检查
    def test_delete_data(self):
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
        message = 'GET /v1/data/<dataName> 正常情况'
        self.client.post(path='/v1/data/%s' % data_name, data={'file': (StringIO(test_case), 'test.csv')})
        # test
        response = self.client.delete(path='/v1/data/%s' % data_name)
        self.assertJsonResponse(response, 200, message='OK')
