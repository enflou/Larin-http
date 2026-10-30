from dataclasses import dataclass
from urllib.parse import urlsplit


class ParseError(Exception):
    pass


@dataclass
class Url:
    scheme: str
    host: str
    port: int
    path: str

    @classmethod
    def parse(cls, value):
        try:
            parts = urlsplit(value)
            if parts.scheme not in ("http", "https") or not parts.hostname:
                raise ValueError
            port = parts.port or (443 if parts.scheme == "https" else 80)
            path = parts.path or "/"
            if parts.query:
                path += "?" + parts.query
            return cls(parts.scheme, parts.hostname, port, path)
        except (ValueError, TypeError):
            raise ParseError("Неверный URL")
