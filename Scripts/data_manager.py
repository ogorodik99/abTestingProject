import pandas as pd
import os
from Library.utils import save_pickle, load_pickle


def normalize_data(csv_path, data_dir):
    """Разбивает данные на 2 справочника (3НФ): Пользователи и События."""
    df = pd.read_csv(csv_path)

    # Справочник Пользователей (user_id, group, landing_page)
    users = df[['user_id', 'group', 'landing_page']].drop_duplicates()

    # Справочник Событий (user_id, timestamp, converted)
    events = df[['user_id', 'timestamp', 'converted']]

    save_pickle(users, os.path.join(data_dir, "users.pkl"))
    save_pickle(events, os.path.join(data_dir, "events.pkl"))
    return users, events


def load_data(data_dir):
    users = load_pickle(os.path.join(data_dir, "users.pkl"))
    events = load_pickle(os.path.join(data_dir, "events.pkl"))
    return users, events