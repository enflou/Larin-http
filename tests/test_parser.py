import unittest
from src.http.parser import Parser


class ParserTests(unittest.TestCase):
    def test_request(self):
        request = Parser.parse_request(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        self.assertEqual(request.method, "GET")
        self.assertEqual(request.path, "/")

    def test_post_body(self):
        data = b"POST /echo HTTP/1.1\r\nContent-Length: 3\r\n\r\nabc"
        self.assertEqual(Parser.parse_request(data).body, b"abc")


if __name__ == "__main__":
    unittest.main()
