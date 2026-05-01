import pandas as pd
import matplotlib.pyplot as plt
import os


def save_stats_report(users, events, output_path):
    df = pd.merge(events, users, on='user_id')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("СТАТИСТИЧЕСКИЙ ОТЧЕТ\n\n")
        f.write(df.groupby('group')['converted'].describe().to_string())


def create_plots(users, events, graphics_dir):
    df = pd.merge(events, users, on='user_id')

    # Столбчатая диаграмма
    plt.figure(figsize=(10, 6))
    df.groupby('group')['converted'].mean().plot(kind='bar', color=['blue', 'orange'])
    plt.title('Средняя конверсия по группам')
    plt.savefig(os.path.join(graphics_dir, "conversion_bar.png"))
    plt.close()