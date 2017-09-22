import unittest

from flask import json

from .. import create_app


class IcurveTestCase(unittest.TestCase):
    longMessage = True
    tear_down = []

    def setUp(self):
        self.app = create_app()
        self.assertIsNotNone(self.app)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.assertIsNotNone(self.client)

    def tearDown(self):
        if self.tear_down:
            for func, args in self.tear_down:
                func(args)

    def assertJsonResponse(self, response, status_code=None, header=None, data=None, message=None):
        if status_code is not None:
            self.assertEqual(response.status_code, status_code, message)
        if header is not None:
            resp_headers = {key: value for key, value in response.headers}
            if isinstance(header, list):
                for key in header:
                    self.assertIn(key, resp_headers, message)
            elif isinstance(header, dict):
                for key, value in header.items():
                    self.assertIn(key, resp_headers, message)
                    self.assertEqual(value, resp_headers[key], message)
        try:
            response = json.loads(response.data)
        except Exception as e:
            raise self.failureException('%s : %s' % (e.message, message))
        self.assertIn('msg', response)
        self.assertIn('traceId', response)
        self.assertIn('server', response)
        if data is not None:
            self.assertEqual(json.dumps(response['data']), json.dumps(data))
        if 'data' in response:
            return response['data']
        return {}

import sys
print sys.path