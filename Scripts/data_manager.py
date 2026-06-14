import os
import pandas as pd
from Library.utils import save_pickle, load_pickle


def normalize_data(csv_path, data_dir):
    os.makedirs(data_dir, exist_ok=True)

    df = pd.read_csv(csv_path)
    df["user_id"] = df["user_id"].astype(str)
    df["converted"] = pd.to_numeric(df["converted"], errors="coerce").fillna(0)
    df["converted"] = df["converted"].astype(int)

    users = df[["user_id", "group", "landing_page"]].drop_duplicates()

    events = df[["user_id", "timestamp", "converted"]]

    save_pickle(users, os.path.join(data_dir, "users.pkl"))
    save_pickle(events, os.path.join(data_dir, "events.pkl"))
    return users, events


def load_data(data_dir):
    users = load_pickle(os.path.join(data_dir, "users.pkl"))
    events = load_pickle(os.path.join(data_dir, "events.pkl"))
    return users, events


def load_ab_data(data_dir):
    return pd.read_csv(os.path.join(data_dir, "ab_data.csv"))


def save_ab_data(data_dir, data):
    os.makedirs(data_dir, exist_ok=True)
    data = data[
        ["user_id", "timestamp", "group", "landing_page", "converted"]
    ].copy()
    data["user_id"] = data["user_id"].astype(str)
    data["timestamp"] = data["timestamp"].astype(str)
    data["group"] = data["group"].astype(str)
    data["landing_page"] = data["landing_page"].astype(str)
    data["converted"] = pd.to_numeric(
        data["converted"],
        errors="coerce",
    ).fillna(0)
    data["converted"] = data["converted"].astype(int)
    data.to_csv(os.path.join(data_dir, "ab_data.csv"), index=False)


def load_users(data_dir):
    return load_pickle(os.path.join(data_dir, "users.pkl"))


def load_events(data_dir):
    return load_pickle(os.path.join(data_dir, "events.pkl"))


def save_users(data_dir, users):
    os.makedirs(data_dir, exist_ok=True)
    users = users[["user_id", "group", "landing_page"]].copy()
    users["user_id"] = users["user_id"].astype(str)
    save_pickle(users, os.path.join(data_dir, "users.pkl"))


def save_events(data_dir, events):
    os.makedirs(data_dir, exist_ok=True)
    events = events[["user_id", "timestamp", "converted"]].copy()
    events["user_id"] = events["user_id"].astype(str)
    events["converted"] = pd.to_numeric(
        events["converted"],
        errors="coerce",
    ).fillna(0)
    events["converted"] = events["converted"].astype(int)
    save_pickle(events, os.path.join(data_dir, "events.pkl"))
