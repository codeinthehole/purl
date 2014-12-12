from unittest import TestCase

import purl


class TemplateTests(TestCase):

    def test_basic_expansion(self):
        template = purl.Template('http://example.com{+path,x}/here')
        url = template.expand({'path': '/foo/bar', 'x': 1024})
        self.assertEquals('http://example.com/foo/bar,1024/here',
                          url.as_string())

    def test_github_api_expansion(self):
        template = purl.Template(
            'https://api.github.com/repos/codeinthehole/purl/labels{/name}')
        url = template.expand()
        self.assertEquals(
            'https://api.github.com/repos/codeinthehole/purl/labels',
            url.as_string())
