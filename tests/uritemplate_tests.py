from nose.tools import eq_

import purl


data = [
    ('http://example.com/~{username}', {'username': 'hello'}, 'http://example.com/~hello'),
    # Form-style
    ('http://example.com/foo{?query,number}', {'query': 'mycelium', 'number': 100}, 'http://example.com/foo?query=mycelium&number=100'),
    ('http://example.com/foo{?query,number}', {'number': 100}, 'http://example.com/foo?number=100'),
    ('http://example.com/foo{?query,number}', {}, 'http://example.com/foo'),
    ('http://example.com/foo{?query,number}', None, 'http://example.com/foo'),
]


def expand(template, fields, expected):
    t = purl.Template(template)
    url = t.expand(fields)
    eq_(url.as_string(), expected)


def test_expansion():
    for template, fields, expected in data:
        yield expand, template, fields, expected
