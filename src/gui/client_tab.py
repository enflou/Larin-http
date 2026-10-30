import threading
import tkinter as tk
from tkinter import ttk
from src.client.http_client import HttpClient


class ClientTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        ttk.Label(self, text="URL").pack(anchor="w")
        self.url = ttk.Entry(self)
        self.url.insert(0, "http://example.com")
        self.url.pack(fill="x", pady=4)
        row = ttk.Frame(self)
        row.pack(fill="x")
        self.method = tk.StringVar(value="GET")
        ttk.Combobox(row, textvariable=self.method, values=["GET", "POST"], width=8, state="readonly").pack(side="left")
        ttk.Button(row, text="Отправить", command=self.send).pack(side="left", padx=6)
        ttk.Button(row, text="Очистить", command=self.clear).pack(side="left")
        ttk.Label(self, text="Заголовки (каждая строка: имя: значение)").pack(anchor="w", pady=(10, 0))
        self.headers = tk.Text(self, height=4)
        self.headers.pack(fill="x")
        ttk.Label(self, text="Тело запроса").pack(anchor="w", pady=(8, 0))
        self.body = tk.Text(self, height=5)
        self.body.pack(fill="x")
        ttk.Label(self, text="Ответ").pack(anchor="w", pady=(8, 0))
        self.output = tk.Text(self)
        self.output.pack(fill="both", expand=True)
        self.status = ttk.Label(self, text="")
        self.status.pack(anchor="w")

    def send(self):
        url = self.url.get().strip()
        method = self.method.get()
        headers = {}
        try:
            for line in self.headers.get("1.0", "end").splitlines():
                if line.strip():
                    key, value = line.split(":", 1)
                    headers[key.strip()] = value.strip()
            body = self.body.get("1.0", "end-1c").encode() if method == "POST" else b""
        except ValueError:
            self.output.delete("1.0", "end")
            self.output.insert("end", "Неверный формат заголовков")
            return
        self.status.config(text="Отправка...")
        threading.Thread(target=self._request, args=(method, url, headers, body), daemon=True).start()

    def _request(self, method, url, headers, body):
        try:
            response = HttpClient().send(method, url, headers, body)
            text = f"Статус: {response.status} {response.reason}\n"
            text += "\n".join(f"{k}: {v}" for k, v in response.headers.items())
            text += "\n\n" + response.body.decode("utf-8", errors="replace")
        except Exception as exc:
            text = f"Ошибка: {exc}"
        self.after(0, self._show, text)

    def _show(self, text):
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.status.config(text="Готово")

    def clear(self):
        self.output.delete("1.0", "end")
        self.body.delete("1.0", "end")
        self.headers.delete("1.0", "end")
        self.status.config(text="")
