import os
import sys
import unittest
from htmlmin.middleware import HtmlMinifyMiddleware
from htmlmin.tests import TESTS_DIR
from mocks import RequestMock, ResponseMock

class TestMiddleware(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, TESTS_DIR)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'mock_settings'

    @classmethod
    def tearDownClass(cls):
        sys.path.remove(TESTS_DIR)
        del os.environ['DJANGO_SETTINGS_MODULE']

    def test_middleware_should_minify_only_when_status_code_is_200(self):
        response_mock = ResponseMock()
        response_mock.status_code = 301
        response = HtmlMinifyMiddleware().process_response(RequestMock(), response_mock)

        html_not_minified = "<html>   <body>some text here</body>    </html>"
        self.assertEqual(html_not_minified, response.content)

    def test_middleware_should_be_minify_response_when_mime_type_is_html(self):
        response_mock = ResponseMock()
        response = HtmlMinifyMiddleware().process_response(RequestMock(), response_mock)

        html_minified = "<!DOCTYPE html><html><body>some text here</body></html>"
        self.assertEqual(html_minified, response.content)

    def test_middleware_should_minify_with_any_charset(self):
        response_mock = ResponseMock()
        response_mock['Content-Type'] = 'text/html; charset=utf-8'
        response = HtmlMinifyMiddleware().process_response(RequestMock(), response_mock)

        html_minified = "<!DOCTYPE html><html><body>some text here</body></html>"
        self.assertEqual(html_minified, response.content)

    def test_middleware_should_not_minify_response_when_mime_type_not_is_html(self):
        response_mock = ResponseMock()
        response_mock['Content-Type'] = 'application/json'
        response = HtmlMinifyMiddleware().process_response(RequestMock(), response_mock)

        html_not_minified = "<html>   <body>some text here</body>    </html>"
        self.assertEqual(html_not_minified, response.content)

    def test_middleware_should_not_minify_the_response_on_urls_that_are_configured_to_not_be_minified(self):
        html_not_minified = "<html>   <body>some text here</body>    </html>"
        response_mock = ResponseMock()
        response = HtmlMinifyMiddleware().process_response(RequestMock('/raw/'), response_mock)
        self.assertEqual(html_not_minified, response.content)
