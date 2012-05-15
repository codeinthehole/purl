import urlparse
import urllib
from collections import namedtuple

# To minimise memory consumption, we use a namedtuple to store all instance
# variables, as well as using the __slots__ attribute.
_URLTuple = namedtuple("_URLTuple", "host username password scheme port path query fragment")


def parse(url_str):
    """
    Extract all parts from a URL string and return them as a dictionary
    """
    result = urlparse.urlparse(url_str)
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
        parts = ["%s://" % url.scheme if url.scheme else u'',
                 self.netloc(),
                 url.path,
                 u'?%s' % url.query if url.query else u'',
                 u'#%s' % url.fragment if url.fragment else u'']
        if url.host is None:
            return u''.join(parts[2:])
        return u''.join(parts)

    __str__ = as_string = __unicode__

    # Accessors / Mutators
    # These use the jQuery overloading style whereby they become mutators if
    # extra args are passed

    def netloc(self):
        url = self._tuple
        if url.username and url.password:
            netloc = u'%s:%s@%s' % (url.username, url.password, url.host)
        else:
            netloc = url.host
        if url.port:
            netloc = u'%s:%s' % (netloc, url.port)
        return netloc

    def host(self, value=None):
        if value:
            return URL._mutate(self, host=value)
        return self._tuple.host

    domain = host

    def username(self):
        return self._tuple.username

    def password(self):
        return self._tuple.password

    def subdomains(self, value=None):
        if value is not None:
            return URL._mutate(self, host='.'.join(value))
        return self.host().split('.')

    def subdomain(self, index, value=None):
        if value is not None:
            subdomains = self.subdomains()
            subdomains[index] = value
            return URL._mutate(self, host='.'.join(subdomains))
        return self.subdomains()[index]

    def scheme(self, value=None):
        if value:
            return URL._mutate(self, scheme=value)
        return self._tuple.scheme

    def path(self, value=None):
        if value:
            if not value.startswith('/'):
                value = '/' + value
            return URL._mutate(self, path=value)
        return self._tuple.path

    def query(self, value=None):
        if value:
            return URL._mutate(self, query=value)
        return self._tuple.query

    def port(self, value=None):
        if value:
            return URL._mutate(self, port=value)
        return self._tuple.port

    def fragment(self, value=None):
        if value:
            return URL._mutate(self, fragment=value)
        return self._tuple.fragment

    def path_segment(self, index, value=None, default=None):
        """
        Return the path segment at the given index
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
        if value is not None:
            new_path = '/' + '/'.join(value)
            return URL._mutate(self, path=new_path)
        parts = self._tuple.path.split('/')
        segments = parts[1:]
        if self._tuple.path.endswith('/'):
            segments.pop()
        return tuple(segments)

    def add_path_segment(self, value):
        segments = self.path_segments() + (value,)
        return self.path_segments(segments)

    def has_query_param(self, key):
        return self.query_param(key) is not None

    def has_query_params(self, keys):
        return all([self.has_query_param(k) for k in keys])

    def query_param(self, key, value=None, default=None, as_list=False):
        """
        Return a query parameter for the given key
        """
        parse_result = self.query_params()
        if value is not None:
            parse_result[key] = value
            return URL._mutate(self, query=urllib.urlencode(parse_result,
                                                            doseq=True))
        try:
            result = parse_result[key]
        except KeyError:
            return default
        if as_list:
            return result
        return result[0] if len(result) == 1 else result

    def query_params(self, value=None):
        if value is not None:
            return URL._mutate(self, query=urllib.urlencode(value, doseq=True))
        query = '' if self._tuple.query is None else self._tuple.query
        return urlparse.parse_qs(query, True)

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
