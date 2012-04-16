import urlparse
import urllib


class URL(object):

    def __init__(self, host=None, username=None, password=None, scheme='http',
                 port=None, path='/',
                 query=None, fragment=None):
        self._host = host
        self._username = username
        self._password = password
        self._scheme = scheme
        self._path = path
        self._query = query
        self._port = port
        self._fragment = fragment

    def __unicode__(self):
        parts = ["%s://" % self._scheme if self._scheme else u'',
                 self.netloc(),
                 self._path,
                 u'?%s' % self._query if self._query else u'',
                 u'#%s' % self._fragment if self._fragment else u'']
        if self._host is None:
            return u''.join(parts[2:])
        return u''.join(parts)

    __str__ = __unicode__

    # Accessors / Mutators
    # These use the jQuery overloading style whereby they become mutators if
    # extra args are passed

    def netloc(self):
        if self._username and self._password:
            netloc = u'%s:%s@%s' % (self._username, self._password, self._host)
        else:
            netloc = self._host
        if self._port:
            netloc = u'%s:%s' % (netloc, self._port)
        return netloc

    def host(self, value=None):
        if value:
            return URL._mutate(self, host=value)
        return self._host

    domain = host

    def username(self):
        return self._username

    def password(self):
        return self._password

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
            return URL._mutate(self, query=urllib.urlencode(parse_result))
        try:
            result = parse_result[key]
        except KeyError:
            return default
        if as_list:
            return result
        return result[0] if len(result) == 1 else result

    def query_params(self, value=None):
        if value is not None:
            return URL._mutate(self, query=urllib.urlencode(value))
        query = '' if self._query is None else self._query
        return urlparse.parse_qs(query, True)

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
        netloc_parts = result.netloc.split('@')
        if len(netloc_parts) == 1:
            username = password = None
            host = netloc_parts[0]
        else:
            username, password = netloc_parts[0].split(':')
            host = netloc_parts[1]

        return cls(host=host,
                   username=username,
                   password=password,
                   scheme=result.scheme,
                   port=result.port,
                   path=result.path,
                   query=result.query,
                   fragment=result.fragment)
