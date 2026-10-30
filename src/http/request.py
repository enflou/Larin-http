from dataclasses import dataclass, field


@dataclass
class Request:
    method: str
    path: str
    version: str = "HTTP/1.1"
    headers: dict = field(default_factory=dict)
    body: bytes = b""
