from nose.tools import eq_

import purl

# Define variables as in the RFC (http://tools.ietf.org/html/rfc6570)
level2_vars = {
    'var': 'value',
    'hello': 'Hello World!',
    'path': '/foo/bar'
}
level3_vars = level2_vars.copy()
level3_vars.update({
    'empty': '',
    'x': '1024',
    'y': '768'
})

data = [
    # Level 1
    ('http://example.com/~{username}', {'username': 'hello'}, 'http://example.com/~hello'),
    ('http://example.com/~{username}', {'username': 'hello world'}, 'http://example.com/~hello%20world'),
    # Level 2 - reserved expansion
    ('{+var}', level2_vars, 'value'),
    ('{+hello}', level2_vars, 'Hello%20World!'),
    ('{+path}/here', level2_vars, '/foo/bar/here'),
    ('here?ref={+path}', level2_vars, 'here?ref=/foo/bar'),
    # Level 2 - fragment expansion
    ('X{#var}', level2_vars, 'X#value'),
    ('X{#hello}', level2_vars, 'X#Hello%20World!'),
    # Level 3 - string expansion with multiple variables
    ('map?{x,y}', level3_vars, 'map?1024,768'),
    ('{x,hello,y}', level3_vars, '1024,Hello%20World%21,768'),
    # Level 3 - reserved expansion with multiple variables
    ('{+x,hello,y}', level3_vars, '1024,Hello%20World!,768'),
    ('{+path,x}/here', level3_vars, '/foo/bar,1024/here'),
    # Level 3 - fragment expansion with multiple variables
    ('{#x,hello,y}', level3_vars, '#1024,Hello%20World!,768'),
    ('{#path,x}/here', level3_vars, '#/foo/bar,1024/here'),
    # Level 3 - label expansion
    ('X{.var}', level3_vars, 'X.value'),
    ('X{.x,y}', level3_vars, 'X.1024.768'),
]

old = [
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
