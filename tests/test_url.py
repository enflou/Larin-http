import unittest
from src.http.url import Url, ParseError


class UrlTests(unittest.TestCase):
    def test_full_url(self):
        value = Url.parse("http://host:8080/path?q=1")
        self.assertEqual((value.host, value.port, value.path), ("host", 8080, "/path?q=1"))

    def test_default_port(self):
        self.assertEqual(Url.parse("http://host/path").port, 80)

    def test_bad_url(self):
        with self.assertRaises(ParseError):
            Url.parse("wrong")


if __name__ == "__main__":
    unittest.main()
