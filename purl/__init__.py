import urlparse
import urllib

PORT_HTTP = 80


class URL(object):

    def __init__(self, host=None, scheme='http', port=PORT_HTTP, path='/',
                 query=None, fragment=None):
        self._host = host
        self._scheme = scheme
        self._path = path
        self._query = query
        if port is None:
            port = PORT_HTTP
        self._port = port
        self._fragment = fragment

    def __unicode__(self):
        parts = [u'%s://%s' % (self._scheme, self._host),
                 u':%s' % self._port if self._port != PORT_HTTP else '',
                 self._path,
                 u'?%s' % self._query if self._query else '',
                 u'#%s' % self._fragment if self._fragment else '']
        if self._host is None:
            return ''.join(parts[2:])
        return ''.join(parts)

    __str__ = __unicode__

    # Accessors / Mutators
    # These use the jQuery overloading style whereby they become mutators if
    # extra args are passed

    def host(self, value=None):
        if value:
            return URL._mutate(self, host=value)
        return self._host

    domain = host

    def subdomains(self):
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
        return self._scheme

    def path(self, value=None):
        if value:
            if not value.startswith('/'):
                value = '/' + value
            return URL._mutate(self, path=value)
        return self._path

    def query(self, value=None):
        if value:
            return URL._mutate(self, query=value)
        return self._query

    def port(self, value=None):
        if value:
            return URL._mutate(self, port=value)
        return self._port

    def fragment(self, value=None):
        if value:
            return URL._mutate(self, fragment=value)
        return self._fragment

    def path_segment(self, index, value=None, default=None):
        """
        Return the path segment at the given index
        """
        if value is not None:
            segments = list(self.path_segments())
            segments[index] = value
            new_path = '/' + '/'.join(segments)
            if self._path.endswith('/'):
                new_path += '/'
            return URL._mutate(self, path=new_path)
        try:
            return self.path_segments()[index]
        except IndexError:
            return default

    def path_segments(self):
        parts = self._path.split('/')
        if len(parts) <= 2:
            return default
        segments = parts[1:]
        if self._path.endswith('/'):
            segments.pop()
        return tuple(segments)

    def query_param(self, key, value=None, default=None):
        """
        Return a query parameter for the given key
        """
        parse_result = self.query_params()
        if value is not None:
            parse_result[key] = value
            return URL._mutate(self, query=urllib.urlencode(parse_result))
        try:
            result = parse_result[key]
        except KeyError:
            return default
        return result[0] if len(result) == 1 else result

    def query_params(self, value=None):
        if value is not None:
            return URL._mutate(self, query=urllib.urlencode(value))
        return urlparse.parse_qs(self._query)

    @classmethod
    def _mutate(cls, url, **kwargs):
        args = {'host': url.host(),
                'scheme': url.scheme(),
                'port': url.port(),
                'path': url.path(),
                'query': url.query(),
                'fragment': url.fragment()}
        args.update(kwargs)
        return cls(**args)

    @classmethod
    def from_string(cls, url_str):
        """
        Factory method to create a new instance based on a passed string
        """
        result = urlparse.urlparse(url_str)
        return cls(host=result.netloc,
                   scheme=result.scheme,
                   port=result.port,
                   path=result.path,
                   query=result.query,
                   fragment=result.fragment)
