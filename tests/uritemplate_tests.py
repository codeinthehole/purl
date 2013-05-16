from nose.tools import eq_

import purl


level2_vars = {
    'var': 'value',
    'hello': 'Hello World!',
    'path': '/foo/bar'
}

data = [
    # Level 1
    ('http://example.com/~{username}', {'username': 'hello'}, 'http://example.com/~hello'),
    ('http://example.com/~{username}', {'username': 'hello world'}, 'http://example.com/~hello%20world'),
    # Level 2
    ('{+var}', level2_vars, 'value'),
    ('{+hello}', level2_vars, 'Hello%20World!'),
    ('{+path}/here', level2_vars, '/foo/bar/here'),
    ('here?ref={+path}', level2_vars, 'here?ref=/foo/bar'),
    # Level 2 - fragment expansion
    ('X{#var}', level2_vars, 'X#value'),
    ('X{#hello}', level2_vars, 'X#Hello%20World!'),
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
