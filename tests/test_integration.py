import unittest
import socket
import time
from src.server.http_server import HttpServer
from src.client.http_client import HttpClient


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        probe = socket.socket()
        probe.bind(("127.0.0.1", 0))
        cls.port = probe.getsockname()[1]
        probe.close()
        cls.server = HttpServer(port=cls.port)
        cls.server.start()
        time.sleep(0.1)
        cls.client = HttpClient()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_get(self):
        response = self.client.send("GET", f"http://127.0.0.1:{self.port}/")
        self.assertEqual(response.status, 200)
        self.assertIn(b"Hello", response.body)

    def test_echo(self):
        response = self.client.send("POST", f"http://127.0.0.1:{self.port}/echo",
                                    {"Content-Type": "text/plain"}, b"abc")
        self.assertEqual(response.body, b"abc")


if __name__ == "__main__":
    unittest.main()
