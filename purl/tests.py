from unittest import TestCase

from purl import URL


class ConstructorTests(TestCase):

    def test_url_can_be_created_with_just_host(self):
        u = URL(host='google.com')
        self.assertEqual('http://google.com/', str(u))

    def test_url_can_be_created_with_host_and_schema(self):
        u = URL(host='google.com', scheme='https')
        self.assertEqual('https://google.com/', str(u))

    def test_url_can_be_created_with_host_and_post(self):
        u = URL(host='localhost', port=8000)
        self.assertEqual('http://localhost:8000/', str(u))


class FactoryTests(TestCase):

    def setUp(self):
        self.url_str = 'http://www.google.com/search/?q=testing'
        self.url = URL.from_string(self.url_str)

    def test_scheme(self):
        self.assertEqual('http', self.url.scheme)

    def test_path(self):
        self.assertEqual('/search/', self.url.path)

    def test_host(self):
        self.assertEqual('www.google.com', self.url.host)

    def test_string_version(self):
        self.assertEqual(self.url_str, str(self.url))


class SimpleExtractionTests(TestCase):

    def setUp(self):
        self.url = URL.from_string('http://www.google.com/blog/article/1?q=testing') 

    def test_path_extraction(self):
        self.assertEqual('1', self.url.path_segment(2))

    def test_path_extraction_returns_none_if_index_too_large(self):
        self.assertIsNone(self.url.path_segment(14))

    def test_path_extraction_can_take_default_value(self):
        self.assertEqual('hello', self.url.path_segment(3, 'hello'))

    def test_parameter_extraction(self):
        self.assertEqual('testing', self.url.query_param('q'))

    def test_parameter_extraction_with_default(self):
        self.assertEqual('eggs', self.url.query_param('p', 'eggs'))

    def test_parameter_extraction_is_none_if_not_found(self):
        self.assertIsNone(self.url.query_param('p'))


class NoTrailingSlashTests(TestCase):

    def test_path_extraction_without_trailing_slash(self):
        u = URL(host='google.com', path='/blog/article/1')
        self.assertEqual('1', u.path_segment(2))
