from datetime import datetime, timezone
from email.utils import format_datetime


class Serializer:
    @staticmethod
    def request(method, path, headers, body=b""):
        values = dict(headers)
        values.setdefault("Host", "localhost")
        values.setdefault("Connection", "close")
        values["Content-Length"] = str(len(body))
        head = f"{method} {path} HTTP/1.1\r\n"
        head += "".join(f"{k}: {v}\r\n" for k, v in values.items())
        return (head + "\r\n").encode("iso-8859-1") + body

    @staticmethod
    def response(status, reason, body=b"", content_type="text/plain; charset=utf-8", headers=None):
        values = dict(headers or {})
        values["Content-Type"] = content_type
        values["Content-Length"] = str(len(body))
        values["Date"] = format_datetime(datetime.now(timezone.utc), usegmt=True)
        values["Connection"] = "close"
        head = f"HTTP/1.1 {status} {reason}\r\n"
        head += "".join(f"{k}: {v}\r\n" for k, v in values.items())
        return (head + "\r\n").encode("iso-8859-1") + body
