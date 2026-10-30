from src.http.url import Url
from src.http.serializer import Serializer
from src.http.parser import Parser
from src.net.tcp_client import TcpClient


class HttpClient:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.tcp = TcpClient()

    def send(self, method, url, headers=None, body=b""):
        target = Url.parse(url)
        raw = Serializer.request(method, target.path, headers or {}, body)
        with self._connection(target) as sock:
            sock.send_all(raw)
            data = b""
            while True:
                try:
                    part = sock.recv(4096)
                except TimeoutError:
                    raise
                if not part:
                    break
                data += part
                if len(data) > 10_000_000:
                    raise ValueError("Ответ слишком большой")
        return Parser.parse_response(data)

    def _connection(self, target):
        from src.net.socket_wrapper import Socket
        sock = self.tcp.connect(target.host, target.port, self.timeout, target.scheme == "https")
        return Socket(sock)
