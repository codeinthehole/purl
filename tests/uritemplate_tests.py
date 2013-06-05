import collections

from nose.tools import eq_

from purl.template import expand

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
level4_vars = level2_vars.copy()
level4_vars.update({
    'list': ['red', 'green', 'blue'],
    'keys': [('semi', ';'), ('dot', '.'), ('comma', ',')]
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
    # Level 3 - path segments, slash prefixed
    ('{/var}', level3_vars, '/value'),
    ('{/var,x}/here', level3_vars, '/value/1024/here'),
    # Level 3 - path segments, semi-colon prefixed
    ('{;x,y}', level3_vars, ';x=1024;y=768'),
    ('{;x,y,empty}', level3_vars, ';x=1024;y=768;empty'),
    # Level 3 - form-style query, ampersand-separated
    ('{?x,y}', level3_vars, '?x=1024&y=768'),
    ('{?x,y,empty}', level3_vars, '?x=1024&y=768&empty='),
    # Level 3 - form-style query continuation
    ('?fixed=yes{&x}', level3_vars, '?fixed=yes&x=1024'),
    ('{&x,y,empty}', level3_vars, '&x=1024&y=768&empty='),
    # Level 4 - string expansion with value modifiers
    ('{var:3}', level4_vars, 'val'),
    ('{var:30}', level4_vars, 'value'),
    ('{list}', level4_vars, 'red,green,blue'),
    ('{list*}', level4_vars, 'red,green,blue'),
    ('{keys}', level4_vars, 'semi,%3B,dot,.,comma,%2C'),
    ('{keys*}', level4_vars, 'semi=%3B,dot=.,comma=%2C'),
    # Level 4 - reserved expansion with value modifiers
    ('{+path:6}/here', level4_vars, '/foo/b/here'),
    ('{+list}', level4_vars, 'red,green,blue'),
    ('{+list*}', level4_vars, 'red,green,blue'),
    ('{+keys}', level4_vars, 'semi,;,dot,.,comma,,'),
    ('{+keys*}', level4_vars, 'semi=;,dot=.,comma=,'),
    # Level 4 - fragment expansion with value modifiers
    ('{#path:6}/here', level4_vars, '#/foo/b/here'),
    ('{#list}', level4_vars, '#red,green,blue'),
    ('{#list*}', level4_vars, '#red,green,blue'),
    ('{#keys}', level4_vars, '#semi,;,dot,.,comma,,'),
    ('{#keys*}', level4_vars, '#semi=;,dot=.,comma=,'),
    # Level 4 - label expansion, dot-prefixed
    ('X{.var:3}', level4_vars, 'X.val'),
    ('X{.list}', level4_vars, 'X.red,green,blue'),
    ('X{.list*}', level4_vars, 'X.red.green.blue'),
    ('X{.keys}', level4_vars, 'X.semi,%3B,dot,.,comma,%2C'),
    ('X{.keys*}', level4_vars, 'X.semi=%3B.dot=..comma=%2C'),
    # Level 4 - path segments, slash-prefixed
    ('{/var:1,var}', level4_vars, '/v/value'),
    ('{/list}', level4_vars, '/red,green,blue'),
    ('{/list*}', level4_vars, '/red/green/blue'),
    ('{/list*,path:4}', level4_vars, '/red/green/blue/%2Ffoo'),
    ('{/keys}', level4_vars, '/semi,%3B,dot,.,comma,%2C'),
    ('{/keys*}', level4_vars, '/semi=%3B/dot=./comma=%2C'),
    # Level 5 - path-style parameters, semicolon-prefixed
    ('{;hello:5}', level4_vars, ';hello=Hello'),
    ('{;list}', level4_vars, ';list=red,green,blue'),
    ('{;list*}', level4_vars, ';list=red;list=green;list=blue'),
    ('{;keys}', level4_vars, ';keys=semi,%3B,dot,.,comma,%2C'),
    ('{;keys*}', level4_vars, ';semi=%3B;dot=.;comma=%2C'),
]
_data = [
    ('{;list}', level4_vars, ';list=red,green,blue'),
]


def assert_expansion(template, fields, expected):
    eq_(expand(template, fields), expected)


def test_expansion():
    for template, fields, expected in data:
        yield assert_expansion, template, fields, expected
