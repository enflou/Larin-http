class Socket:
    def __init__(self, sock):
        self.sock = sock

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def send_all(self, data):
        self.sock.sendall(data)

    def recv(self, size):
        return self.sock.recv(size)
