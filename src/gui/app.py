import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.client_tab import ClientTab
from src.gui.server_tab import ServerTab


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HTTP клиент и сервер")
        self.root.geometry("850x600")
        tabs = ttk.Notebook(self.root)
        tabs.pack(fill="both", expand=True)
        tabs.add(ClientTab(tabs), text="Клиент")
        tabs.add(ServerTab(tabs), text="Сервер")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Notebook):
                for tab in child.winfo_children():
                    if hasattr(tab, "stop_server"):
                        tab.stop_server()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
