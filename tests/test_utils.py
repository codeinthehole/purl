from purl.url import to_utf8, to_unicode


class TestUnicodeHelper:

    def test_convert_int_to_bytes(self):
        assert b'1024' == to_utf8(1024)

    def test_convert_int_to_unicode(self):
        assert '1024' == to_unicode(1024)
