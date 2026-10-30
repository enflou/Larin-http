from src.http.request import Request
from src.http.response import Response


class Parser:
    @staticmethod
    def parse_request(data):
        try:
            head, body = data.split(b"\r\n\r\n", 1)
            lines = head.decode("iso-8859-1").split("\r\n")
            method, path, version = lines[0].split(" ", 2)
            headers = {}
            for line in lines[1:]:
                if ":" not in line:
                    raise ValueError
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
            length = int(headers.get("Content-Length", "0"))
            if length > len(body):
                raise ValueError
            return Request(method.upper(), path, version, headers, body[:length])
        except Exception as exc:
            raise ValueError("Некорректный HTTP-запрос") from exc

    @staticmethod
    def parse_response(data):
        head, body = data.split(b"\r\n\r\n", 1)
        lines = head.decode("iso-8859-1").split("\r\n")
        version, status, *reason = lines[0].split(" ")
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()
        length = int(headers.get("Content-Length", len(body)))
        return Response(int(status), " ".join(reason), version, headers, body[:length])
