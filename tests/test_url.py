# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from purl import URL
import pytest

import pickle

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


class TestConstructor:
    def test_url_can_be_created_with_just_host(self):
        u = URL(host="google.com")
        assert "http://google.com/" == str(u)

    def test_url_can_be_created_with_host_and_schema(self):
        u = URL(host="google.com", scheme="https")
        assert "https://google.com/" == str(u)

    def test_url_can_be_created_with_host_and_post(self):
        u = URL(host="localhost", port=8000)
        assert "http://localhost:8000/" == str(u)

    def test_url_can_be_created_with_username_only(self):
        u = URL(
            scheme="postgres",
            username="user",
            host="127.0.0.1",
            port="5432",
            path="/db_name",
        )
        assert "postgres://user@127.0.0.1:5432/db_name" == str(u)

    def test_no_args_to_constructor(self):
        u = URL()
        assert "/" == str(u)

    def test_as_string(self):
        assert "/" == URL().as_string()

    def test_full_url_can_be_used_as_first_param(self):
        u = URL("https://github.com")
        assert "https://github.com" == u.as_string()

    def test_kwargs_take_priority_when_used_with_full_url(self):
        u = URL("https://github.com", scheme="http")
        assert "http://github.com" == u.as_string()

    def test_creation_with_host_and_path(self):
        u = URL(host="localhost", path="boo")
        assert "http://localhost/boo" == str(u)

    def test_creation_with_host_and_path_2(self):
        u = URL(host="localhost").add_path_segment("boo")
        assert "http://localhost/boo" == str(u)


class TestMoreFactory:
    def test_extracting_query_param(self):
        url_str = "https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&token=EC-6469953681606921P&AMT=200&CURRENCYCODE=GBP&RETURNURL=http%3A%2F%2Fexample.com%2Fcheckout%2Fpaypal%2Fresponse%2Fsuccess%2F&CANCELURL=http%3A%2F%2Fexample.com%2Fcheckout%2Fpaypal%2Fresponse%2Fcancel%2F"
        url = URL.from_string(url_str)
        return_url = url.query_param("RETURNURL")
        assert "http://example.com/checkout/paypal/response/success/" == return_url


class TestFactory:

    url_str = "http://www.google.com/search/?q=testing#fragment"
    url = URL.from_string(url_str)

    def test_scheme(self):
        assert "http" == self.url.scheme()

    def test_fragment(self):
        assert "fragment" == self.url.fragment()

    def test_path(self):
        assert "/search/" == self.url.path()

    def test_host(self):
        assert "www.google.com" == self.url.host()

    def test_string_version(self):
        assert self.url_str == str(self.url)


class TestEdgeCaseExtraction:
    def test_no_equals_sign_means_empty_string(self):
        url = URL.from_string("http://www.google.com/blog/article/1?q")
        assert "" == url.query_param("q")

    def test_list_extraction(self):
        url = URL.from_string("http://www.google.com/?q=1&q=2&q=3")
        assert ["1" == "2", "3"], url.query_param("q")

    def test_username_extraction(self):
        url = URL.from_string("ftp://user:pw@ftp.host")
        assert "user" == url.username()
        assert "pw" == url.password()

    def test_username_in_unicode_repr(self):
        u = "ftp://user:pw@ftp.host"
        url = URL.from_string(u)
        assert u == str(url)

    def test_auth_in_netloc(self):
        url = URL.from_string("ftp://user:pw@ftp.host")
        assert "user:pw@ftp.host" == url.netloc()

    def test_auth_with_special_char(self):
        url = URL.from_string("ftp://user:b@z@ftp.host")
        assert "user" == url.username()
        assert "b@z" == url.password()

    def test_port_in_netloc(self):
        url = URL.from_string("http://localhost:5000")
        assert "localhost" == url.host()
        assert 5000 == url.port()

    def test_passwordless_netloc(self):
        url = URL.from_string("postgres://user@127.0.0.1:5432/db_name")
        assert "user" == url.username()
        assert url.password() is None

    def test_unicode_username_and_password(self):
        url = URL.from_string("postgres://jeść:niejeść@127.0.0.1:5432/db_name")
        assert "jeść" == url.username()
        assert "niejeść" == url.password()

    def test_unicode_username_only(self):
        url = URL.from_string("postgres://jeść@127.0.0.1:5432/db_name")
        assert "jeść" == url.username()
        assert url.password() is None

    def test_port_for_https_url(self):
        url = URL.from_string("https://github.com")
        assert None == url.port()


class TestSimpleExtraction:
    url = URL.from_string("http://www.google.com/blog/article/1?q=testing")

    def test_has_actual_param(self):
        assert self.url.has_query_param("q") is True

    def test_remove_query_param(self):
        new_url = self.url.remove_query_param("q")
        assert "http://www.google.com/blog/article/1" == new_url.as_string()

    def test_has_query_params(self):
        assert self.url.has_query_params(["q"]) is True

    def test_has_query_params_negative(self):
        assert self.url.has_query_params(["q", "r"]) is False

    def test_netloc(self):
        assert "www.google.com" == self.url.netloc()

    def test_path_extraction(self):
        assert "1" == self.url.path_segment(2)

    def test_port_defaults_to_none(self):
        assert self.url.port() is None

    def test_scheme(self):
        assert "http" == self.url.scheme()

    def test_host(self):
        assert "www.google.com" == self.url.host()

    def test_domain(self):
        assert "www.google.com" == self.url.domain()

    def test_subdomains(self):
        assert ["www" == "google", "com"], self.url.subdomains()

    def test_subdomain(self):
        assert "www" == self.url.subdomain(0)

    def test_invalid_subdomain_raises_indexerror(self):
        with pytest.raises(IndexError):
            self.url.subdomain(10)

    def test_path(self):
        assert "/blog/article/1" == self.url.path()

    def test_query(self):
        assert "q=testing" == self.url.query()

    def test_query_param_as_list(self):
        assert ["testing"] == self.url.query_param("q", as_list=True)

    def test_query_params(self):
        assert {"q": ["testing"]} == self.url.query_params()

    def test_path_extraction_returns_none_if_index_too_large(self):
        assert self.url.path_segment(14) is None

    def test_path_extraction_can_take_default_value(self):
        assert "hello" == self.url.path_segment(3, default="hello")

    def test_parameter_extraction(self):
        assert "testing" == self.url.query_param("q")

    def test_parameter_extraction_with_default(self):
        assert "eggs" == self.url.query_param("p", default="eggs")

    def test_parameter_extraction_is_none_if_not_found(self):
        assert self.url.query_param("p") is None

    def test_path_segments(self):
        assert ("blog", "article", "1") == self.url.path_segments()

    def test_relative(self):
        assert "/blog/article/1?q=testing" == str(self.url.relative())


class TestNoTrailingSlash:
    def test_path_extraction_without_trailing_slash(self):
        u = URL(host="google.com", path="/blog/article/1")
        assert "1" == u.path_segment(2)


class TestBuilder:
    def test_setting_list_as_query_params(self):
        first = URL.from_string("?q=testing")
        second = URL().query_params(first.query_params())
        assert first.query() == second.query()

    def test_add_path_segment(self):
        url = (
            URL("http://example.com")
            .add_path_segment("one")
            .add_path_segment("two")
            .add_path_segment("three")
        )
        assert "/one/two/three" == url.path()

    def test_setting_single_item_list_as_query_param(self):
        url = URL().query_param("q", ["testing"])
        assert "testing" == url.query_param("q")

    def test_setting_list_as_query_param(self):
        url = URL().query_param("q", ["testing", "eggs"])
        assert ["testing" == "eggs"], url.query_param("q", as_list=True)

    def test_build_relative_url(self):
        url = URL().path("searching")
        assert "/searching" == str(url)

    def test_build_relative_url_with_params(self):
        URL().path("/searching").query_param("q", "testing")

    def test_build_with_path_segments(self):
        u = URL().path_segments(["path", "to", "page"])
        assert "/path/to/page" == u.as_string()

    def test_set_fragment(self):
        url = URL.from_string("http://www.google.com/").fragment("hello")
        assert "hello" == url.fragment()

    def test_set_scheme(self):
        url = URL.from_string("http://www.google.com/").scheme("https")
        assert "https" == url.scheme()

    def test_set_host(self):
        url = URL.from_string("http://www.google.com/").host("maps.google.com")
        assert "maps.google.com" == url.host()

    def test_set_path(self):
        url = URL.from_string("http://www.google.com/").path("search")
        assert "/search" == url.path()

    def test_set_path_with_special_chars(self):
        url = URL.from_string("http://www.google.com/").path("search something")
        assert "/search%20something" == url.path()

    def test_set_query(self):
        url = URL.from_string("http://www.google.com/").query("q=testing")
        assert "testing" == url.query_param("q")

    def test_set_port(self):
        url = URL.from_string("http://www.google.com/").port(8000)
        assert 8000 == url.port()

    def test_set_path_segment(self):
        url = URL.from_string("http://www.google.com/a/b/c/").path_segment(1, "d")
        assert "/a/d/c/" == url.path()

    def test_set_query_param(self):
        url = URL.from_string("http://www.google.com/search").query_param(
            "q", "testing"
        )
        assert "testing" == url.query_param("q")

    def test_set_query_params(self):
        url = URL.from_string("http://www.google.com/search").query_params(
            {"q": "testing"}
        )
        assert "testing" == url.query_param("q")

    def test_set_subdomain(self):
        url = URL.from_string("http://www.google.com/search").subdomain(0, "www2")
        assert "www2" == url.subdomain(0)

    def test_set_subdomains(self):
        url = URL().subdomains(["www", "google", "com"])
        assert "http://www.google.com/" == str(url)

    def test_remove_domain(self):
        url = URL("https://example.com/hello?x=100")
        new = url.domain("")
        assert "/hello?x=100" == str(new)

    def test_remove_port(self):
        url = URL("https://example.com/hello?x=100")
        new = url.port("")
        assert "https://example.com/hello?x=100" == str(new)


class TestMisc:
    def test_url_can_be_used_as_key_in_dict(self):
        u = URL.from_string("http://google.com")
        {u: 0}

    def test_equality_comparison(self):
        assert URL.from_string("http://google.com") == URL.from_string(
            "http://google.com"
        )

    def test_negative_equality_comparison(self):
        assert URL.from_string("http://google.com") != URL.from_string(
            "https://google.com"
        )

    def test_urls_are_hashable(self):
        u = URL.from_string("http://google.com")
        hash(u)

    def test_urls_can_be_pickled(self):
        u = URL.from_string("http://google.com")
        pickle.dumps(u)

    def test_urls_can_be_pickled_and_restored(self):
        u = URL.from_string("http://google.com")
        pickled = pickle.dumps(u)
        v = pickle.loads(pickled)
        assert u == v


class TestQueryParamList:
    def test_set_list(self):
        base = URL("http://127.0.0.1/")
        url = base.query_param("q", ["something", "else"])
        values = url.query_param("q", as_list=True)
        assert ["something" == "else"], values

    def test_remove_item_from_list(self):
        base = URL("http://127.0.0.1/?q=a&q=b")
        url = base.remove_query_param("q", "a")
        values = url.query_param("q", as_list=True)
        assert ["b"] == values

    def test_append_to_existing_list(self):
        base = URL("http://127.0.0.1/?q=a&q=b")
        url = base.append_query_param("q", "c")
        values = url.query_param("q", as_list=True)
        assert ["a", "b", "c"] == values

    def test_append_to_nonexistant_list(self):
        base = URL("http://127.0.0.1/?q=a&q=b")
        url = base.append_query_param("p", "c")
        values = url.query_param("p", as_list=True)
        assert ["c"] == values


class TestUnicodeExtraction:
    def test_get_query_param_ascii_url(self):
        unicode_param = "значение"

        # Python 2.6 requires bytes for quote
        urlencoded_param = quote(unicode_param.encode("utf8"))
        url = "http://www.google.com/blog/article/1?q=" + urlencoded_param

        ascii_url = URL.from_string(url.encode("ascii"))
        param = ascii_url.query_param("q")
        assert param == unicode_param

    def test_get_query_param_unicode_url(self):
        unicode_param = "значение"

        # Python 2.6 requires bytes for quote
        urlencoded_param = quote(unicode_param.encode("utf8"))
        url = "http://www.google.com/blog/article/1?q=" + urlencoded_param

        # django request.get_full_path() returns url as unicode
        unicode_url = URL.from_string(url)

        param = unicode_url.query_param("q")
        assert param == unicode_param


class TestUnicode:
    base = URL("http://127.0.0.1/")
    text = "ć"
    bytes = text.encode("utf8")

    def test_set_unicode_query_param_value(self):
        url = self.base.query_param("q", self.text)
        assert self.text == url.query_param("q")

    def test_set_bytestring_query_param_value(self):
        url = self.base.query_param("q", self.bytes)
        assert self.text == url.query_param("q")

    def test_set_unicode_query_param_key(self):
        url = self.base.query_param(self.text, "value")
        assert "value" == url.query_param(self.text)

    def test_set_bytestring_query_param_key(self):
        url = self.base.query_param(self.bytes, "value")
        assert "value" == url.query_param(self.text)

    def test_append_unicode_query_param(self):
        url = self.base.append_query_param("q", self.text)
        assert self.text == url.query_param("q")

    def test_append_bytestring_query_param(self):
        url = self.base.append_query_param("q", self.bytes)
        assert self.text == url.query_param("q")

    def test_set_unicode_query_params(self):
        url = self.base.query_params({"q": self.text})
        assert self.text == url.query_param("q")

    def test_set_bytestring_query_params(self):
        url = self.base.query_params({"q": self.bytes})
        assert self.text == url.query_param("q")

    def test_add_unicode_path_segment(self):
        url = self.base.add_path_segment(self.text)
        assert self.text == url.path_segment(0)

    def test_add_bytestring_path_segment(self):
        url = self.base.add_path_segment(self.bytes)
        assert self.text == url.path_segment(0)

    def test_add_unicode_fragment(self):
        url = self.base.fragment(self.text)
        assert self.text == url.fragment()


class QuotedSlashesTests:
    def test_slashes_in_path(self):
        u = URL().add_path_segment("test/egg")
        assert u.as_string() == "/test%2Fegg"

    def test_slashes_in_path(self):
        u = URL("/something").path_segment(0, "test/egg")
        assert u.as_string() == "/test%2Fegg"
