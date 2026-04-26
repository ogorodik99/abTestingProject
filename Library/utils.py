import configparser
import os
import pickle


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config


def save_config(config, config_path):
    with open(config_path, "w", encoding="utf-8") as f:
        config.write(f)


def save_pickle(data, filepath):
    with open(filepath, "wb") as f:
        pickle.dump(data, f)


def load_pickle(filepath):
    with open(filepath, "rb") as f:
        return pickle.load(f)


def ensure_dirs(paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)


def format_float(value, decimals=4):
    return f"{value:.{decimals}f}"


def save_text_report(text, filepath):

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
