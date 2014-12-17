from unittest import TestCase

from purl.url import to_utf8, to_unicode


class TestUnicodeHelper(TestCase):

    def test_convert_int_to_bytes(self):
        self.assertEqual('1024', to_utf8(1024))

    def test_convert_int_to_unicode(self):
        self.assertEqual(u'1024', to_unicode(1024))
