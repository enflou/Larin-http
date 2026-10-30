import tkinter as tk
from tkinter import ttk, messagebox
import queue
import webbrowser
from src.server.http_server import HttpServer


class ServerTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        row = ttk.Frame(self)
        row.pack(fill="x")
        ttk.Label(row, text="Порт").pack(side="left")
        self.port = ttk.Entry(row, width=10)
        self.port.insert(0, "8080")
        self.port.pack(side="left", padx=5)
        ttk.Button(row, text="Запустить", command=self.start_server).pack(side="left", padx=4)
        ttk.Button(row, text="Остановить", command=self.stop_server).pack(side="left")
        ttk.Button(row, text="Открыть в браузере", command=lambda: webbrowser.open("http://localhost:" + self.port.get())).pack(side="left", padx=4)
        self.state = ttk.Label(self, text="Сервер остановлен")
        self.state.pack(anchor="w", pady=8)
        self.log = tk.Text(self)
        self.log.pack(fill="both", expand=True)
        ttk.Button(self, text="Очистить лог", command=lambda: self.log.delete("1.0", "end")).pack(anchor="e", pady=5)
        self.messages = queue.Queue()
        self.server = None
        self.after(100, self.update_log)

    def start_server(self):
        try:
            port = int(self.port.get())
            if not 1 <= port <= 65535:
                raise ValueError
            self.server = HttpServer(port=port, on_log=self.messages.put)
            self.server.start()
            self.state.config(text=f"Сервер запущен на порту {port}")
        except Exception as exc:
            messagebox.showerror("Ошибка", str(exc))

    def stop_server(self):
        if self.server:
            self.server.stop()
            self.server = None
        self.state.config(text="Сервер остановлен")

    def update_log(self):
        while not self.messages.empty():
            self.log.insert("end", self.messages.get() + "\n")
            self.log.see("end")
        self.after(100, self.update_log)
