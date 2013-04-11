from __future__ import unicode_literals

__title__ = 'purl'
__version__ = '0.6'
__author__ = 'David Winterbottom'
__license__ = 'MIT'

try:
    from urllib.parse import parse_qs, urlencode, urlparse
except ImportError:
    from urllib import urlencode
    from urlparse import parse_qs, urlparse
from collections import namedtuple


# Python 2/3 compatibility
import sys
PY3 = sys.version_info[0] == 3

if PY3:
    def b(s):
        return s
else:
    def b(s):
        return s.encode('utf8')


# To minimise memory consumption, we use a namedtuple to store all instance
# variables, as well as using the __slots__ attribute.
_URLTuple = namedtuple("_URLTuple", "host username password scheme port path query fragment")


def parse(url_str):
    """
    Extract all parts from a URL string and return them as a dictionary
    """
    result = urlparse(url_str)
    netloc_parts = result.netloc.split('@')
    if len(netloc_parts) == 1:
        username = password = None
        host = netloc_parts[0]
    else:
        username, password = netloc_parts[0].split(':')
        host = netloc_parts[1]

    if host and ':' in host:
        host = host.split(':')[0]

    return {'host': host,
            'username': username,
            'password': password,
            'scheme': result.scheme,
            'port': result.port,
            'path': result.path,
            'query': result.query,
            'fragment': result.fragment}


class URL(object):
    """
    The constructor can be used in two ways:

    1. Pass a URL string::

        >>> URL('http://www.google.com/search?q=testing').as_string()
        u'http://www.google.com/search?q=testing'

    2. Pass keyword arguments::

        >>> URL(host='www.google.com', path='/search', query='q=testing').as_string()
        u'http://www.google.com/search?q=testing'

    If you pass both a URL string and keyword args, then the values of keyword
    args take precedence.
    """

    __slots__ = ("_tuple",)

    def __init__(self, url_str=None, host=None, username=None, password=None,
                 scheme=None, port=None, path=None, query=None, fragment=None):
        if url_str is not None:
            params = parse(url_str)
        else:
            # Defaults
            params = {'scheme': 'http',
                      'username': None,
                      'password': None,
                      'host': None,
                      'port': None,
                      'path': '/',
                      'query': None,
                      'fragment': None}

        # Kwargs override the url_str
        for var in 'host username password scheme port path query fragment'.split():
            if locals()[var] is not None:
                params[var] = locals()[var]

        self._tuple = _URLTuple(params['host'],
                                params['username'],
                                params['password'],
                                params['scheme'],
                                params['port'],
                                params['path'],
                                params['query'],
                                params['fragment'])

    def __eq__(self, other):
        return self._tuple == other._tuple

    def __ne__(self, other):
        return self._tuple != other._tuple

    def __getstate__(self):
        return tuple(self._tuple)

    def __setstate__(self, state):
        self._tuple = _URLTuple(*state)

    def __hash__(self):
        return hash(self._tuple)

    def __repr__(self):
        return str(self._tuple)

    def __unicode__(self):
        url = self._tuple
        parts = ["%s://" % url.scheme if url.scheme else '',
                 self.netloc(),
                 url.path,
                 '?%s' % url.query if url.query else '',
                 '#%s' % url.fragment if url.fragment else '']
        if url.host is None:
            return ''.join(parts[2:])
        return ''.join(parts)

    __str__ = as_string = __unicode__

    # Accessors / Mutators
    # These use the jQuery overloading style whereby they become mutators if
    # extra args are passed

    def netloc(self):
        """
        Return the netloc
        """
        url = self._tuple
        if url.username and url.password:
            netloc = '%s:%s@%s' % (url.username, url.password, url.host)
        else:
            netloc = url.host
        if url.port:
            netloc = '%s:%s' % (netloc, url.port)
        return netloc

    def host(self, value=None):
        """
        Return the host

        :param string value: new host string
        """
        if value:
            return URL._mutate(self, host=value)
        return self._tuple.host

    domain = host

    def username(self):
        """
        Return the username
        """
        return self._tuple.username

    def password(self):
        """
        Return the password
        """
        return self._tuple.password

    def subdomains(self, value=None):
        """
        Returns a list of subdomains or set the subdomains and returns a
        new :class:`URL` instance.

        :param list value: a list of subdomains
        """
        if value is not None:
            return URL._mutate(self, host='.'.join(value))
        return self.host().split('.')

    def subdomain(self, index, value=None):
        """
        Return a subdomain or set a new value and return a new :class:`URL`
        instance.

        :param integer index: 0-indexed subdomain
        :param string value: New subdomain
        """
        if value is not None:
            subdomains = self.subdomains()
            subdomains[index] = value
            return URL._mutate(self, host='.'.join(subdomains))
        return self.subdomains()[index]

    def scheme(self, value=None):
        """
        Return or set the scheme.

        :param string value: the new scheme to use
        :returns: string or new :class:`URL` instance
        """
        if value:
            return URL._mutate(self, scheme=value)
        return self._tuple.scheme

    def path(self, value=None):
        """
        Return or set the path

        :param string value: the new path to use
        :returns: string or new :class:`URL` instance
        """
        if value:
            if not value.startswith('/'):
                value = '/' + value
            return URL._mutate(self, path=value)
        return self._tuple.path

    def query(self, value=None):
        """
        Return or set the query string

        :param string value: the new query string to use
        :returns: string or new :class:`URL` instance
        """
        if value:
            return URL._mutate(self, query=value)
        return self._tuple.query

    def port(self, value=None):
        """
        Return or set the port

        :param string value: the new port to use
        :returns: string or new :class:`URL` instance
        """
        if value:
            return URL._mutate(self, port=value)
        return self._tuple.port

    def fragment(self, value=None):
        """
        Return or set the fragment (hash)

        :param string value: the new fragment to use
        :returns: string or new :class:`URL` instance
        """
        if value:
            return URL._mutate(self, fragment=value)
        return self._tuple.fragment

    # ====
    # Path
    # ====

    def path_segment(self, index, value=None, default=None):
        """
        Return the path segment at the given index

        :param integer index:
        :param string value: the new segment value
        :param string default: the default value to return if no path segment exists with the given index
        """
        if value is not None:
            segments = list(self.path_segments())
            segments[index] = value
            new_path = '/' + '/'.join(segments)
            if self._tuple.path.endswith('/'):
                new_path += '/'
            return URL._mutate(self, path=new_path)
        try:
            return self.path_segments()[index]
        except IndexError:
            return default

    def path_segments(self, value=None):
        """
        Return the path segments

        :param list value: the new path segments to use
        """
        if value is not None:
            new_path = '/' + '/'.join(value)
            return URL._mutate(self, path=new_path)
        parts = self._tuple.path.split('/')
        segments = parts[1:]
        if self._tuple.path.endswith('/'):
            segments.pop()
        return tuple(segments)

    def add_path_segment(self, value):
        """
        Add a new path segment to the end of the current string

        :param string value: the new path segment to use

        Example::

            >>> u = URL('http://example.com/foo/')
            >>> u.add_path_segment('bar').as_string()
            u'http://example.com/foo/bar'
        """
        segments = self.path_segments() + (value,)
        return self.path_segments(segments)

    # ============
    # Query params
    # ============

    def has_query_param(self, key):
        """
        Test if a given query parameter is present

        :param string key: key to test for
        """
        return self.query_param(key) is not None

    def has_query_params(self, keys):
        """
        Test if a given set of query parameters are present

        :param list keys: keys to test for
        """
        return all([self.has_query_param(k) for k in keys])

    def query_param(self, key, value=None, default=None, as_list=False):
        """
        Return or set a query parameter for the given key

        The value can be a list.

        :param string key: key to look for
        :param string default: value to return if ``key`` isn't found
        :param boolean as_list: whether to return the values as a list
        :param string value: the new query parameter to use
        """
        parse_result = self.query_params()
        if value is not None:
            parse_result[key] = value
            return URL._mutate(self, query=urlencode(parse_result, doseq=True))
        try:
            result = parse_result[key]
        except KeyError:
            return default
        if as_list:
            return result
        return result[0] if len(result) == 1 else result

    def append_query_param(self, key, value):
        """
        Append a query parameter

        :param string key: The query param key
        :param string value: The new value
        """
        values = self.query_param(key, as_list=True, default=[])
        values.append(value)
        return self.query_param(key, values)

    def query_params(self, value=None):
        """
        Return or set a dictionary of query params

        :param dict value: new dictionary of values
        """
        if value is not None:
            return URL._mutate(self, query=urlencode(value, doseq=True))
        query = '' if self._tuple.query is None else self._tuple.query
        return parse_qs(query, True)

    def remove_query_param(self, key, value=None):
        """
        Remove a query param from a URL

        Set the value parameter if removing from a list.

        :param string key: The key to delete
        :param string value: The value of the param to delete (of more than one)
        """
        parse_result = self.query_params()
        if value is not None:
            index = parse_result[key].index(value)
            del parse_result[key][index]
        else:
            del parse_result[key]
        return URL._mutate(self, query=urlencode(parse_result, doseq=True))

    @classmethod
    def _mutate(cls, url, **kwargs):
        args = url._tuple._asdict()
        args.update(kwargs)
        return cls(**args)

    @classmethod
    def from_string(cls, url_str):
        """
        Factory method to create a new instance based on a passed string

        This method is deprecated now
        """
        return cls(url_str)
