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

    def test_no_args_to_constructor(self):
        u = URL()
        self.assertEqual('/', str(u))


class MoreFactoryTests(TestCase):

    def setUp(self):
        self.url_str = 'https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&token=EC-6469953681606921P&AMT=200&CURRENCYCODE=GBP&RETURNURL=http%3A%2F%2Fexample.com%2Fcheckout%2Fpaypal%2Fresponse%2Fsuccess%2F&CANCELURL=http%3A%2F%2Fexample.com%2Fcheckout%2Fpaypal%2Fresponse%2Fcancel%2F'
        self.url = URL.from_string(self.url_str)

    def test_extracting_query_param(self):
        return_url = self.url.query_param('RETURNURL')
        self.assertEqual('http://example.com/checkout/paypal/response/success/',
                         return_url)


class FactoryTests(TestCase):

    def setUp(self):
        self.url_str = 'http://www.google.com/search/?q=testing#fragment'
        self.url = URL.from_string(self.url_str)

    def test_scheme(self):
        self.assertEqual('http', self.url.scheme())

    def test_fragment(self):
        self.assertEqual('fragment', self.url.fragment())

    def test_path(self):
        self.assertEqual('/search/', self.url.path())

    def test_host(self):
        self.assertEqual('www.google.com', self.url.host())

    def test_string_version(self):
        self.assertEqual(self.url_str, str(self.url))


class EdgeCaseExtractionTests(TestCase):

    def test_no_equals_sign_means_empty_string(self):
        url = URL.from_string('http://www.google.com/blog/article/1?q') 
        self.assertEqual('', url.query_param('q'))

    def test_list_extraction(self):
        url = URL.from_string('http://www.google.com/?q=1&q=2&q=3') 
        self.assertEqual(['1', '2', '3'], url.query_param('q'))

    def test_username_extraction(self):
        url = URL.from_string('ftp://user:pw@ftp.host') 
        self.assertEqual('user', url.username())
        self.assertEqual('pw', url.password())

    def test_username_in_unicode_repr(self):
        u = 'ftp://user:pw@ftp.host'
        url = URL.from_string(u) 
        self.assertEqual(u, str(url))

    def test_auth_in_netloc(self):
        url = URL.from_string('ftp://user:pw@ftp.host') 
        self.assertEqual('user:pw@ftp.host', url.netloc())


class SimpleExtractionTests(TestCase):

    def setUp(self):
        self.url = URL.from_string('http://www.google.com/blog/article/1?q=testing') 

    def test_has_actual_param(self):
        self.assertTrue(self.url.has_query_param('q'))

    def test_has_query_params(self):
        self.assertTrue(self.url.has_query_params(['q']))

    def test_has_query_params_negative(self):
        self.assertFalse(self.url.has_query_params(['q', 'r']))

    def test_netloc(self):
        self.assertEqual('www.google.com', self.url.netloc())

    def test_path_extraction(self):
        self.assertEqual('1', self.url.path_segment(2))

    def test_port_defaults_to_none(self):
        self.assertIsNone(self.url.port())

    def test_scheme(self):
        self.assertEqual('http', self.url.scheme())

    def test_host(self):
        self.assertEqual('www.google.com', self.url.host())

    def test_domain(self):
        self.assertEqual('www.google.com', self.url.domain())

    def test_subdomains(self):
        self.assertEqual(['www', 'google', 'com'], self.url.subdomains())

    def test_subdomain(self):
        self.assertEqual('www', self.url.subdomain(0))

    def test_invalid_subdomain_raises_indexerror(self):
        with self.assertRaises(IndexError):
            self.url.subdomain(10)

    def test_path(self):
        self.assertEqual('/blog/article/1', self.url.path())

    def test_query(self):
        self.assertEqual('q=testing', self.url.query())

    def test_query_param_as_list(self):
        self.assertEqual(['testing'], self.url.query_param('q', as_list=True))

    def test_query_params(self):
        self.assertEqual({'q': ['testing']}, self.url.query_params())

    def test_path_extraction_returns_none_if_index_too_large(self):
        self.assertIsNone(self.url.path_segment(14))

    def test_path_extraction_can_take_default_value(self):
        self.assertEqual('hello', self.url.path_segment(3, default='hello'))

    def test_parameter_extraction(self):
        self.assertEqual('testing', self.url.query_param('q'))

    def test_parameter_extraction_with_default(self):
        self.assertEqual('eggs', self.url.query_param('p', default='eggs'))

    def test_parameter_extraction_is_none_if_not_found(self):
        self.assertIsNone(self.url.query_param('p'))

    def test_path_segments(self):
        self.assertEqual(('blog', 'article', '1'), self.url.path_segments())


class NoTrailingSlashTests(TestCase):

    def test_path_extraction_without_trailing_slash(self):
        u = URL(host='google.com', path='/blog/article/1')
        self.assertEqual('1', u.path_segment(2))


class BuilderTests(TestCase):
    
    def test_build_relative_url(self):
        url = URL().path('searching')
        self.assertEqual('/searching', str(url))

    def test_set_fragment(self):
        url = URL.from_string('http://www.google.com/').fragment('hello')
        self.assertEqual('hello', url.fragment())

    def test_set_scheme(self):
        url = URL.from_string('http://www.google.com/').scheme('https')
        self.assertEqual('https', url.scheme())

    def test_set_host(self):
        url = URL.from_string('http://www.google.com/').host('maps.google.com')
        self.assertEqual('maps.google.com', url.host())

    def test_set_path(self):
        url = URL.from_string('http://www.google.com/').path('search')
        self.assertEqual('/search', url.path())

    def test_set_query(self):
        url = URL.from_string('http://www.google.com/').query('q=testing')
        self.assertEqual('testing', url.query_param('q'))

    def test_set_port(self):
        url = URL.from_string('http://www.google.com/').port(8000)
        self.assertEqual(8000, url.port())

    def test_set_path_segment(self):
        url = URL.from_string('http://www.google.com/a/b/c/').path_segment(1, 'd')
        self.assertEqual('/a/d/c/', url.path())

    def test_set_query_param(self):
        url = URL.from_string('http://www.google.com/search').query_param('q', 'testing')
        self.assertEqual('testing', url.query_param('q'))

    def test_set_query_params(self):
        url = URL.from_string('http://www.google.com/search').query_params({'q': 'testing'})
        self.assertEqual('testing', url.query_param('q'))

    def test_set_subdomain(self):
        url = URL.from_string('http://www.google.com/search').subdomain(0, 'www2')
        self.assertEqual('www2', url.subdomain(0))

    def test_set_subdomains(self):
        url = URL().subdomains(['www', 'google', 'com'])
        self.assertEqual('http://www.google.com/', str(url))
