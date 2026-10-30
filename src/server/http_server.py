import socket
import threading
import time
from src.http.parser import Parser
from src.http.serializer import Serializer
from src.server.router import Router


class HttpServer:
    def __init__(self, host="127.0.0.1", port=8080, on_log=None):
        self.host = host
        self.port = port
        self.on_log = on_log
        self.router = Router()
        self.sock = None
        self.thread = None
        self.running = False

    def start(self):
        if self.running:
            return
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(20)
        self.sock.settimeout(0.5)
        self.running = True
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    def _serve(self):
        while self.running:
            try:
                conn, _ = self.sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(target=self._handle, args=(conn,), daemon=True).start()

    def _handle(self, conn):
        start = time.time()
        with conn:
            try:
                conn.settimeout(3)
                data = b""
                while b"\r\n\r\n" not in data:
                    part = conn.recv(4096)
                    if not part:
                        break
                    data += part
                    if len(data) > 65536:
                        raise ValueError("Слишком большой запрос")
                if b"\r\n\r\n" not in data:
                    raise ValueError("Некорректный запрос")
                head, body = data.split(b"\r\n\r\n", 1)
                length = 0
                for line in head.decode("iso-8859-1").split("\r\n")[1:]:
                    if line.lower().startswith("content-length:"):
                        length = int(line.split(":", 1)[1].strip())
                while len(body) < length:
                    part = conn.recv(min(4096, length - len(body)))
                    if not part:
                        break
                    body += part
                request = Parser.parse_request(head + b"\r\n\r\n" + body)
                response = self.router.dispatch(request)
                raw = Serializer.response(response.status, response.reason or "OK",
                                          response.body,
                                          response.headers.get("Content-Type", "text/plain; charset=utf-8"))
                conn.sendall(raw)
                status = response.status
                method, path = request.method, request.path
            except Exception:
                raw = Serializer.response(400, "Bad Request", b"400 Bad Request")
                try:
                    conn.sendall(raw)
                except OSError:
                    pass
                status, method, path = 400, "-", "-"
            if self.on_log:
                self.on_log(f"{method} {path} {status} {int((time.time()-start)*1000)} мс")

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close()
            self.sock = None
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
