# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os
import win32api

running = False

# ------------------ LÓGICA ------------------

def get_idle_time():
    idle = win32api.GetTickCount() - win32api.GetLastInputInfo()
    return max(0, idle)

def shutdown_pc():
    os.system("shutdown /s /t 0")

def monitor_idle(seconds, label):
    global running

    idle_at_start = get_idle_time() / 1000

    for remaining in range(seconds, 0, -1):
        if not running:
            root.after(0, lambda: label.config(text="Detenido manualmente."))
            return

        current_idle = get_idle_time() / 1000

        if current_idle < idle_at_start - 0.5:
            running = False
            root.after(0, lambda: label.config(
                text="✋ Actividad detectada. Cancelado."))
            return

        root.after(0, lambda r=remaining: label.config(
            text=f"Apagando en {r} segundos..."))
        time.sleep(1)

    if running:
        root.after(0, lambda: label.config(text="Sin actividad. Apagando..."))
        shutdown_pc()

def start_monitor():
    global running

    if running:
        status_label.config(text="Ya está en ejecución")
        return

    try:
        seconds = int(entry.get())
        if seconds <= 0:
            status_label.config(text="Ingresá un número mayor a 0")
            return
        running = True
        status_label.config(text="Monitoreando...")

        t = threading.Thread(target=monitor_idle, args=(seconds, status_label))
        t.daemon = True
        t.start()
    except ValueError:
        status_label.config(text="Número inválido")

def stop_monitor():
    global running
    running = False
    status_label.config(text="Detenido.")

def set_seconds(value):
    entry.delete(0, tk.END)
    entry.insert(0, str(value))

# ------------------ UI ------------------

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

root = tk.Tk()
root.title("Auto Shutdown AFK")
root.iconbitmap(resource_path("icon.ico"))
root.geometry("340x410")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("default")
style.configure("TButton", font=("Calibri", 12), padding=10)
style.map("TButton", background=[("active", "#3a3a3a")])
style.configure("TEntry",
                fieldbackground="#2a2a2a",
                foreground="#ffffff",
                insertcolor="#ffffff")

container = tk.Frame(root, bg="#1e1e1e")
container.pack(expand=True, fill="both", padx=10, pady=10)

title = tk.Label(container,
                 text="Auto Apagado",
                 font=("Calibri", 30, "bold"),
                 fg="white",
                 bg="#1e1e1e")
title.pack(pady=(10, 4))

label = tk.Label(container,
                 text="Tiempo en segundos",
                 font=("Calibri", 11, "bold"),
                 fg="#B4B4B4",
                 bg="#1e1e1e")
label.pack(pady=(0, 4))

entry = ttk.Entry(container, font=("Calibri", 12), justify="center")
entry.pack(pady=(0, 8), ipady=5)
entry.insert(0, "600")

btn_frame = tk.Frame(container, bg="#1e1e1e")
btn_frame.pack(pady=(0, 12))

start_btn = tk.Button(btn_frame,
                      text="Iniciar",
                      bg="#2e7d32",
                      fg="white",
                      activebackground="#388e3c",
                      font=("Calibri", 15, "bold"),
                      width=12,
                      height=2,
                      command=start_monitor,
                      relief="flat")
start_btn.pack(side="left", padx=8)

stop_btn = tk.Button(btn_frame,
                     text="Detener",
                     bg="#c62828",
                     fg="white",
                     activebackground="#e53935",
                     font=("Calibri", 15, "bold"),
                     width=12,
                     height=2,
                     command=stop_monitor,
                     relief="flat")
stop_btn.pack(side="left", padx=8)

status_label = tk.Label(container,
                        text="",
                        font=("Calibri", 11, "bold"),
                        fg="#aaaaaa",
                        bg="#1e1e1e")
status_label.pack(pady=(0, 12))

sep = tk.Frame(container, bg="#444444", height=1)
sep.pack(fill="x", pady=(0, 10))

ejemplos_title = tk.Label(container,
                          text="Ejemplos rápidos",
                          font=("Calibri", 11, "bold"),
                          fg="#888888",
                          bg="#1e1e1e")
ejemplos_title.pack(pady=(0, 6))

ejemplos = [
    ("1 min",   60),
    ("5 min",   300),
    ("10 min",  600),
    ("15 min",  900),
    ("30 min",  1800),
    ("1 hora",  3600),
    ("2 horas", 7200),
    ("3 horas", 10800),
    ("4 horas", 14400),
]

ejemplos_frame = tk.Frame(container, bg="#1e1e1e")
ejemplos_frame.pack()

for i, (texto, valor) in enumerate(ejemplos):
    btn = tk.Button(ejemplos_frame,
                    text=texto,
                    bg="#2a2a2a",
                    fg="#cccccc",
                    activebackground="#3a3a3a",
                    activeforeground="white",
                    font=("Calibri", 10),
                    width=9,
                    relief="flat",
                    command=lambda v=valor: set_seconds(v))
    row = i // 3
    col = i % 3
    btn.grid(row=row, column=col, padx=4, pady=3)

    btn.bind("<Enter>", lambda e: e.widget.config(bg="#3a3a3a"))
    btn.bind("<Leave>", lambda e: e.widget.config(bg="#2a2a2a"))

root.mainloop()