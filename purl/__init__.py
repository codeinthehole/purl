import urlparse

PORT_HTTP = 80


class URL(object):

    def __init__(self, host, scheme='http', port=PORT_HTTP, path='/', query=None):
        self.host = host
        self.scheme = scheme
        self.path = path
        self.query = query
        if port is None:
            port = PORT_HTTP
        self.port = port

    def __unicode__(self):
        parts = [u'%s://%s' % (self.scheme, self.host),
                 u':%s' % self.port if self.port != PORT_HTTP else '',
                 self.path,
                 u'?%s' % self.query if self.query else '']
        return ''.join(parts)

    __str__ = __unicode__

    def path_segment(self, index, default=None):
        """
        Return the path segment at the given index
        """
        parts = self.path.split('/')
        if len(parts) <= 2:
            return default
        segments = parts[1:]
        if self.path.endswith('/'):
            segments.pop()
        try:
            return segments[index]
        except IndexError:
            return default

    def query_param(self, key, default=None):
        """
        Return a query parameter for the given key
        """
        try:
            result = urlparse.parse_qs(self.query)[key]
        except KeyError:
            return default
        return result[0] if len(result) == 1 else result

    @classmethod
    def from_string(cls, url_str):
        result = urlparse.urlparse(url_str)
        return cls(host=result.netloc,
                   scheme=result.scheme,
                   port=result.port,
                   path=result.path,
                   query=result.query)


