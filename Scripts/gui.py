import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

from Scripts.config import CFG


MAIN_BG = "#F2F2F2"
TEXT_COLOR = "#222222"
SECOND_TEXT = "#555555"
BUTTON_BG = "#E6E6E6"
ACCENT_BG = "#3F7FCC"
MAX_VISIBLE_ROWS = 1000


def create_main_window(
    on_analyze,
    on_load_csv,
    on_show_plots,
    on_load_ab_data,
    on_save_ab_data,
):
    root = tk.Tk()
    root.title("CTR")
    root.geometry(f"{CFG['main_width']}x{CFG['main_height']}")
    root.minsize(720, 480)
    root.configure(bg=MAIN_BG)

    _configure_styles(root)

    result_text = tk.StringVar(value="Здесь появится CTR по группам.")
    graph_path = tk.StringVar(value="")
    status_text = tk.StringVar(value="Готово")

    def run_load_csv():
        csv_path = filedialog.askopenfilename(
            parent=root,
            title="Выберите CSV-файл",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
        )
        if not csv_path:
            return

        try:
            status_text.set("Считаю CTR...")
            graph_path.set("")
            root.update_idletasks()
            result = on_load_csv(csv_path)
            result_text.set(_extract_result_text(result))
            graph_path.set(_extract_graph_path(result))
            status_text.set("CTR рассчитан")
        except Exception as error:
            status_text.set("Ошибка расчета")
            messagebox.showerror("Ошибка", str(error))

    def run_analysis():
        try:
            status_text.set("Считаю CTR...")
            root.update_idletasks()
            result = on_analyze()
            result_text.set(_extract_result_text(result))
            graph_path.set(_extract_graph_path(result))
            status_text.set("CTR рассчитан")
            messagebox.showinfo("CTR", "CTR рассчитан.")
        except Exception as error:
            status_text.set("Ошибка расчета")
            messagebox.showerror("Ошибка", str(error))

    def run_show_plots():
        try:
            status_text.set("Открываю графики...")
            root.update_idletasks()
            on_show_plots()
            status_text.set("Графики открыты")
        except Exception as error:
            status_text.set("Ошибка открытия графиков")
            messagebox.showerror("Ошибка", str(error))

    def open_ab_data_editor():
        _open_ab_data_window(
            root,
            on_load_ab_data,
            on_save_ab_data,
            status_text,
        )

    _create_menu(
        root,
        run_load_csv,
        run_analysis,
        run_show_plots,
        open_ab_data_editor,
    )

    shell = ttk.Frame(root, style="App.TFrame", padding=16)
    shell.pack(fill=tk.BOTH, expand=True)
    shell.columnconfigure(0, weight=1)
    shell.rowconfigure(2, weight=1)

    _create_header(shell)
    _create_action_bar(
        shell,
        run_load_csv,
        run_analysis,
        run_show_plots,
        open_ab_data_editor,
    )
    _create_content(shell, result_text, graph_path)
    _create_status_bar(shell, status_text)

    return root


def _configure_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    font = (CFG["main_font"], CFG["main_size"])
    title_font = (CFG["main_font"], CFG["header_size"] + 4, "bold")
    small_font = (CFG["main_font"], max(CFG["main_size"] - 1, 9))

    style.configure("App.TFrame", background=MAIN_BG)
    style.configure("Box.TFrame", background="#FFFFFF", relief=tk.GROOVE)
    style.configure(
        "Title.TLabel",
        background=MAIN_BG,
        foreground=TEXT_COLOR,
        font=title_font,
    )
    style.configure(
        "Text.TLabel",
        background=MAIN_BG,
        foreground=SECOND_TEXT,
        font=font,
    )
    style.configure(
        "BoxTitle.TLabel",
        background="#FFFFFF",
        foreground=TEXT_COLOR,
        font=(CFG["main_font"], CFG["header_size"], "bold"),
    )
    style.configure(
        "Status.TLabel",
        background=MAIN_BG,
        foreground=SECOND_TEXT,
        font=small_font,
    )
    style.configure(
        "Accent.TButton",
        background=ACCENT_BG,
        foreground="#FFFFFF",
        font=(CFG["main_font"], CFG["btn_size"]),
        padding=(10, 6),
    )
    style.configure(
        "Simple.TButton",
        background=BUTTON_BG,
        foreground=TEXT_COLOR,
        font=(CFG["main_font"], CFG["btn_size"]),
        padding=(10, 6),
    )


def _create_menu(
    root,
    run_load_csv,
    run_analysis,
    run_show_plots,
    open_ab_data_editor,
):
    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Загрузить CSV", command=run_load_csv)
    file_menu.add_command(label="Редактировать ab_data", command=open_ab_data_editor)
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=root.quit)
    menubar.add_cascade(label="Файл", menu=file_menu)

    ctr_menu = tk.Menu(menubar, tearoff=0)
    ctr_menu.add_command(label="Посчитать CTR", command=run_analysis)
    ctr_menu.add_command(label="Показать графики", command=run_show_plots)
    menubar.add_cascade(label="CTR", menu=ctr_menu)

    root.config(menu=menubar)


def _extract_result_text(result):
    if isinstance(result, dict):
        return result.get("text", "")

    return str(result)


def _extract_graph_path(result):
    if isinstance(result, dict):
        return result.get("graph_path", "")

    return ""


def _create_header(parent):
    header = ttk.Frame(parent, style="App.TFrame")
    header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
    header.columnconfigure(0, weight=1)

    ttk.Label(
        header,
        text="CTR",
        style="Title.TLabel",
    ).grid(row=0, column=0, sticky="w")

    ttk.Label(
        header,
        text="Расчет CTR и простые графики по группам.",
        style="Text.TLabel",
    ).grid(row=1, column=0, sticky="w", pady=(4, 0))


def _create_action_bar(
    parent,
    run_load_csv,
    run_analysis,
    run_show_plots,
    open_ab_data_editor,
):
    panel = ttk.Frame(parent, style="Box.TFrame", padding=12)
    panel.grid(row=1, column=0, sticky="ew", pady=(0, 12))

    buttons = (
        ("Загрузить CSV", run_load_csv, "Simple.TButton"),
        ("Редактировать ab_data", open_ab_data_editor, "Simple.TButton"),
        ("Посчитать CTR", run_analysis, "Accent.TButton"),
        ("Графики", run_show_plots, "Simple.TButton"),
    )

    for index, (text, command, style) in enumerate(buttons):
        panel.columnconfigure(index, weight=1)
        ttk.Button(
            panel,
            text=text,
            style=style,
            command=command,
        ).grid(row=0, column=index, sticky="ew", padx=4)


def _create_content(parent, result_text, graph_path):
    content = ttk.Frame(parent, style="App.TFrame")
    content.grid(row=2, column=0, sticky="nsew")
    content.columnconfigure(0, weight=2)
    content.columnconfigure(1, weight=1)
    content.rowconfigure(0, weight=1)

    report_panel = ttk.Frame(content, style="Box.TFrame", padding=12)
    report_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    report_panel.columnconfigure(0, weight=1)
    report_panel.rowconfigure(1, weight=1)

    ttk.Label(
        report_panel,
        text="Результат",
        style="BoxTitle.TLabel",
    ).grid(row=0, column=0, sticky="w", pady=(0, 8))

    result = tk.Text(
        report_panel,
        height=12,
        wrap="word",
        bg="#FFFFFF",
        fg=TEXT_COLOR,
        relief=tk.SOLID,
        borderwidth=1,
        padx=8,
        pady=8,
        font=(CFG["main_font"], CFG["main_size"]),
    )
    result.grid(row=1, column=0, sticky="nsew")
    result.insert("1.0", result_text.get())
    result.config(state=tk.DISABLED)

    scrollbar = ttk.Scrollbar(report_panel, command=result.yview)
    scrollbar.grid(row=1, column=1, sticky="ns")
    result.configure(yscrollcommand=scrollbar.set)

    graph_panel = ttk.Frame(content, style="Box.TFrame", padding=12)
    graph_panel.grid(row=0, column=1, sticky="nsew")
    graph_panel.columnconfigure(0, weight=1)
    graph_panel.rowconfigure(1, weight=1)

    ttk.Label(
        graph_panel,
        text="Графики",
        style="BoxTitle.TLabel",
    ).grid(row=0, column=0, sticky="w", pady=(0, 8))

    graph_label = tk.Label(
        graph_panel,
        text="Графика пока нет",
        bg="#FFFFFF",
        fg=SECOND_TEXT,
        relief=tk.SOLID,
        borderwidth=1,
        font=(CFG["main_font"], CFG["main_size"]),
        justify=tk.CENTER,
        wraplength=220,
    )
    graph_label.grid(row=1, column=0, sticky="nsew")
    graph_label.image = None
    graph_label.bind(
        "<Button-1>",
        lambda _event: _open_graph_window(graph_panel, graph_path.get()),
    )

    def update_graph(*_):
        path = graph_path.get()
        if not path or not os.path.exists(path):
            graph_label.config(
                image="",
                text="Графика пока нет",
                cursor="arrow",
            )
            graph_label.image = None
            return

        image = tk.PhotoImage(file=path)
        max_width = 260
        max_height = 230
        scale = max(
            1,
            (image.width() + max_width - 1) // max_width,
            (image.height() + max_height - 1) // max_height,
        )
        if scale > 1:
            image = image.subsample(scale, scale)

        graph_label.config(image=image, text="", cursor="hand2")
        graph_label.image = image

    def update_result(*_):
        result.config(state=tk.NORMAL)
        result.delete("1.0", tk.END)
        result.insert("1.0", result_text.get())
        result.config(state=tk.DISABLED)

    graph_path.trace_add("write", update_graph)
    result_text.trace_add("write", update_result)


def _open_graph_window(parent, graph_file):
    if not graph_file or not os.path.exists(graph_file):
        messagebox.showinfo(
            "Графики",
            "Сначала посчитайте CTR.",
            parent=parent,
        )
        return

    window = tk.Toplevel(parent)
    window.title("Графики CTR")
    window.geometry(f"{CFG['rep_width']}x{CFG['rep_height']}")
    window.minsize(700, 420)
    window.configure(bg=MAIN_BG)
    window.transient(parent.winfo_toplevel())

    content = ttk.Frame(window, style="App.TFrame", padding=12)
    content.pack(fill=tk.BOTH, expand=True)
    content.columnconfigure(0, weight=1)
    content.rowconfigure(1, weight=1)

    ttk.Label(
        content,
        text="Графики CTR",
        style="Title.TLabel",
    ).grid(row=0, column=0, sticky="w", pady=(0, 8))

    image = tk.PhotoImage(file=graph_file)
    graph = tk.Label(
        content,
        image=image,
        bg="#FFFFFF",
        relief=tk.SOLID,
        borderwidth=1,
    )
    graph.image = image
    graph.grid(row=1, column=0, sticky="nsew")


def _open_ab_data_window(parent, load_ab_data, save_ab_data, status_text):
    columns = ("user_id", "timestamp", "group", "landing_page", "converted")
    rows = []

    window = tk.Toplevel(parent)
    window.title("Редактировать ab_data")
    window.geometry(f"{CFG['ref_width']}x{CFG['ref_height']}")
    window.minsize(760, 460)
    window.configure(bg=MAIN_BG)
    window.transient(parent)

    content = ttk.Frame(window, style="App.TFrame", padding=12)
    content.pack(fill=tk.BOTH, expand=True)
    content.columnconfigure(0, weight=1)
    content.rowconfigure(1, weight=1)

    ttk.Label(
        content,
        text="Редактировать ab_data",
        style="Title.TLabel",
    ).grid(row=0, column=0, sticky="w", pady=(0, 8))

    table_frame = ttk.Frame(content, style="Box.TFrame", padding=8)
    table_frame.grid(row=1, column=0, sticky="nsew")
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        selectmode="extended",
    )
    tree.grid(row=0, column=0, sticky="nsew")

    widths = {
        "user_id": 90,
        "timestamp": 190,
        "group": 110,
        "landing_page": 130,
        "converted": 90,
    }
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=widths[column], minwidth=70, stretch=True)

    y_scroll = ttk.Scrollbar(
        table_frame,
        orient=tk.VERTICAL,
        command=tree.yview,
    )
    x_scroll = ttk.Scrollbar(
        table_frame,
        orient=tk.HORIZONTAL,
        command=tree.xview,
    )
    tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
    y_scroll.grid(row=0, column=1, sticky="ns")
    x_scroll.grid(row=1, column=0, sticky="ew")

    form = ttk.Frame(content, style="Box.TFrame", padding=8)
    form.grid(row=2, column=0, sticky="ew", pady=(10, 0))

    entries = {}
    for index, column in enumerate(columns):
        form.columnconfigure(index, weight=1)
        ttk.Label(
            form,
            text=column,
            style="BoxTitle.TLabel",
        ).grid(row=0, column=index, sticky="w", padx=(0, 8))

        entry = ttk.Entry(form)
        entry.grid(row=1, column=index, sticky="ew", padx=(0, 8))
        entries[column] = entry

    actions = ttk.Frame(content, style="App.TFrame")
    actions.grid(row=3, column=0, sticky="ew", pady=(10, 0))
    actions.columnconfigure(6, weight=1)

    info_text = tk.StringVar()
    ttk.Label(
        actions,
        textvariable=info_text,
        style="Status.TLabel",
    ).grid(row=0, column=6, sticky="e")

    def current_values():
        return {
            column: entries[column].get().strip()
            for column in columns
        }

    def validate(values):
        empty_columns = [
            column
            for column, value in values.items()
            if value == ""
        ]
        if empty_columns:
            messagebox.showwarning(
                "ab_data",
                "Заполните поля: " + ", ".join(empty_columns),
                parent=window,
            )
            return False

        if values["converted"] not in {"0", "1"}:
            messagebox.showwarning(
                "ab_data",
                "Поле converted должно быть 0 или 1.",
                parent=window,
            )
            return False

        return True

    def clear_form():
        for entry in entries.values():
            entry.delete(0, tk.END)

    def refresh_table():
        tree.delete(*tree.get_children())
        visible_rows = rows[:MAX_VISIBLE_ROWS]

        for index, row in enumerate(visible_rows):
            values = [row.get(column, "") for column in columns]
            tree.insert("", tk.END, iid=str(index), values=values)

        hidden_count = max(len(rows) - len(visible_rows), 0)
        if hidden_count:
            info_text.set(
                f"Показано {len(visible_rows)} из {len(rows)} строк"
            )
        else:
            info_text.set(f"Строк: {len(rows)}")

    def load_rows():
        nonlocal rows
        frame = load_ab_data()
        rows = (
            frame.loc[:, list(columns)]
            .fillna("")
            .astype(str)
            .to_dict(orient="records")
        )
        refresh_table()
        clear_form()
        status_text.set("ab_data загружен")

    def selected_index():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning(
                "ab_data",
                "Выберите строку в таблице.",
                parent=window,
            )
            return None

        return int(selected[0])

    def selected_indexes():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning(
                "ab_data",
                "Выберите строки в таблице.",
                parent=window,
            )
            return []

        return sorted([int(item) for item in selected], reverse=True)

    def fill_form_from_selection(_event=None):
        index = selected_index()
        if index is None:
            return

        clear_form()
        row = rows[index]
        for column in columns:
            entries[column].insert(0, row.get(column, ""))

    def add_row():
        values = current_values()
        if not validate(values):
            return

        rows.insert(0, values)
        refresh_table()
        clear_form()
        status_text.set("Строка добавлена")

    def update_row():
        index = selected_index()
        if index is None:
            return

        values = current_values()
        if not validate(values):
            return

        rows[index] = values
        refresh_table()
        tree.selection_set(str(index))
        status_text.set("Строка изменена")

    def delete_rows():
        indexes = selected_indexes()
        if not indexes:
            return

        if not messagebox.askyesno(
            "ab_data",
            f"Удалить выбранные строки: {len(indexes)}?",
            parent=window,
        ):
            return

        for index in indexes:
            del rows[index]

        save_ab_data(pd.DataFrame(rows, columns=columns))
        refresh_table()
        clear_form()
        status_text.set("Строки удалены и файл сохранен")

    def delete_all_rows():
        if not rows:
            return

        if not messagebox.askyesno(
            "ab_data",
            "Удалить все строки из ab_data.csv?",
            parent=window,
        ):
            return

        rows.clear()
        save_ab_data(pd.DataFrame(rows, columns=columns))
        refresh_table()
        clear_form()
        status_text.set("Все строки удалены и файл сохранен")

    def save_rows():
        frame = pd.DataFrame(rows, columns=columns)
        save_ab_data(frame)
        status_text.set("ab_data сохранен")
        messagebox.showinfo("ab_data", "Файл сохранен.", parent=window)

    buttons = (
        ("Добавить", add_row, "Accent.TButton"),
        ("Изменить", update_row, "Simple.TButton"),
        ("Удалить", delete_rows, "Simple.TButton"),
        ("Очистить все", delete_all_rows, "Simple.TButton"),
        ("Сохранить", save_rows, "Simple.TButton"),
        ("Загрузить", load_rows, "Simple.TButton"),
    )

    for index, (text, command, style) in enumerate(buttons):
        ttk.Button(
            actions,
            text=text,
            style=style,
            command=command,
        ).grid(row=0, column=index, padx=(0, 6))

    tree.bind("<<TreeviewSelect>>", fill_form_from_selection)
    load_rows()


def _create_status_bar(parent, status_text):
    status = ttk.Frame(parent, style="App.TFrame")
    status.grid(row=3, column=0, sticky="ew", pady=(10, 0))
    status.columnconfigure(0, weight=1)

    ttk.Label(
        status,
        textvariable=status_text,
        style="Status.TLabel",
    ).grid(row=0, column=0, sticky="w")
