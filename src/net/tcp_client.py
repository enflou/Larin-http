import socket
import ssl


class TcpClient:
    def connect(self, host, port, timeout=5, use_ssl=False):
        sock = socket.create_connection((host, port), timeout)
        if use_ssl:
            sock = ssl.create_default_context().wrap_socket(sock, server_hostname=host)
        sock.settimeout(timeout)
        return sock
