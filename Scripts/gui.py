import tkinter as tk
from tkinter import ttk, messagebox
from Scripts.config import CFG


def create_main_window(on_import, on_analyze):
    root = tk.Tk()
    root.title("A/B CTR")
    root.geometry(f"{CFG['main_width']}x{CFG['main_height']}")
    root.configure(bg=CFG['bg_color'])

    # Меню
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Импорт CSV", command=on_import)
    file_menu.add_command(label="Выход", command=root.quit)
    menubar.add_cascade(label="Файл", menu=file_menu)

    root.config(menu=menubar)

    # Кнопка анализа
    btn = tk.Button(root, text="Запустить анализ", bg=CFG['btn_color'],
                    fg=CFG['btn_text'], command=on_analyze)
    btn.pack(pady=20)

    return root