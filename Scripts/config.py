import importlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Library"))

read_config = importlib.import_module("utils").read_config

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.ini")


def load_cfg():
    raw = read_config(CONFIG_PATH)

    cfg = {
        "bg_color": raw.get("COLORS", "bg_color", fallback="#F0F4F8"),
        "btn_color": raw.get("COLORS", "btn_color", fallback="#4A90D9"),
        "btn_text": raw.get("COLORS", "btn_text_color", fallback="#FFFFFF"),
        "header_color": raw.get("COLORS", "header_color", fallback="#2C3E50"),
        "table_bg": raw.get("COLORS", "table_bg", fallback="#FFFFFF"),
        "table_fg": raw.get("COLORS", "table_fg", fallback="#2C3E50"),
        "select_bg": raw.get("COLORS", "select_bg", fallback="#AED6F1"),

        "main_font": raw.get("FONTS", "main_font", fallback="Calibri"),
        "main_size": raw.getint("FONTS", "main_size", fallback=11),
        "header_size": raw.getint("FONTS", "header_size", fallback=13),
        "btn_size": raw.getint("FONTS", "btn_size", fallback=11),

        "main_width": raw.getint("WINDOW", "main_width", fallback=1100),
        "main_height": raw.getint("WINDOW", "main_height", fallback=700),
        "ref_width": raw.getint("WINDOW", "ref_width", fallback=800),
        "ref_height": raw.getint("WINDOW", "ref_height", fallback=500),
        "rep_width": raw.getint("WINDOW", "report_width", fallback=950),
        "rep_height": raw.getint("WINDOW", "report_height", fallback=600),

        "data_dir": _abs(raw.get("PATHS", "data_dir", fallback="../Data")),
        "output_dir": _abs(
            raw.get("PATHS", "output_dir", fallback="../Output")
        ),
        "graphics_dir": _abs(
            raw.get("PATHS", "graphics_dir", fallback="../Graphics")
        ),
    }
    return cfg


def _abs(rel_path):
    base = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(base, rel_path))


def save_cfg(cfg):
    import configparser
    raw = configparser.ConfigParser()
    raw["COLORS"] = {
        "bg_color": cfg["bg_color"],
        "btn_color": cfg["btn_color"],
        "btn_text_color": cfg["btn_text"],
        "header_color": cfg["header_color"],
        "table_bg": cfg["table_bg"],
        "table_fg": cfg["table_fg"],
        "select_bg": cfg["select_bg"],
    }
    raw["FONTS"] = {
        "main_font": cfg["main_font"],
        "main_size": str(cfg["main_size"]),
        "header_size": str(cfg["header_size"]),
        "btn_size": str(cfg["btn_size"]),
    }
    raw["WINDOW"] = {
        "main_width": str(cfg["main_width"]),
        "main_height": str(cfg["main_height"]),
        "ref_width": str(cfg["ref_width"]),
        "ref_height": str(cfg["ref_height"]),
        "report_width": str(cfg["rep_width"]),
        "report_height": str(cfg["rep_height"]),
    }
    raw["PATHS"] = {
        "data_dir": "../Data",
        "output_dir": "../Output",
        "graphics_dir": "../Graphics",
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        raw.write(f)


CFG = load_cfg()
