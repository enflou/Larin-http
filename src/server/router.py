import json
from datetime import datetime
from src.http.response import Response


class Router:
    def dispatch(self, request):
        path = request.path.split("?", 1)[0]
        if request.method == "GET" and path == "/":
            return Response(200, "OK", headers={"Content-Type": "text/html; charset=utf-8"},
                            body=b"<html><body><h1>Hello</h1></body></html>")
        if request.method == "POST" and path == "/echo":
            return Response(200, "OK", headers={"Content-Type": request.headers.get("Content-Type", "text/plain")},
                            body=request.body)
        if request.method == "GET" and path == "/time":
            body = json.dumps({"time": datetime.now().isoformat()}).encode()
            return Response(200, "OK", headers={"Content-Type": "application/json"}, body=body)
        if request.method == "GET" and path == "/headers":
            body = json.dumps(request.headers, ensure_ascii=False).encode()
            return Response(200, "OK", headers={"Content-Type": "application/json"}, body=body)
        if request.method == "GET" and path.startswith("/status/"):
            try:
                code = int(path.rsplit("/", 1)[1])
                if 100 <= code <= 599:
                    return Response(code, "Custom", body=f"Status {code}".encode())
            except ValueError:
                pass
        return Response(404, "Not Found", body=b"404 Not Found")
