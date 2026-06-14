import importlib
import os

import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "Output")
os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(OUTPUT_DIR, ".matplotlib"),
)
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(OUTPUT_DIR, ".cache"))

plt = importlib.import_module("matplotlib.pyplot")


def save_stats_report(users, events, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = _merge_reference_data(users, events)
    stats = df.groupby("group").agg(
        impressions=("user_id", "count"),
        clicks=("converted", "sum"),
        ctr_percent=("converted", "mean"),
    )
    stats["ctr_percent"] = stats["ctr_percent"] * 100

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("ОТЧЕТ ПО CTR\n\n")
        file.write(
            stats.to_string(formatters={"ctr_percent": "{:.2f}%".format})
        )


def create_plots(users, events, graphics_dir):
    df = _merge_reference_data(users, events)
    metrics = df.groupby("group").agg(
        users=("user_id", "count"),
        clicks=("converted", "sum"),
    )
    metrics["ctr"] = metrics["clicks"] / metrics["users"]
    return save_ctr_graph({"metrics": metrics}, graphics_dir)


def save_ctr_graph(result, graphics_dir):
    os.makedirs(graphics_dir, exist_ok=True)
    output_path = os.path.join(graphics_dir, "ctr_graph.png")
    fig = create_ctr_figure(result)
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def save_ab_test_dashboard(result, graphics_dir):
    return save_ctr_graph(result, graphics_dir)


def show_ctr_graph(result):
    fig = create_ctr_figure(result)
    fig.show()
    plt.show()


def show_ab_test_dashboard(result):
    show_ctr_graph(result)


def create_ctr_figure(result):
    metrics = result["metrics"]
    groups = metrics.index.tolist()
    ctr = metrics["ctr"].to_numpy(dtype=float) * 100

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    colors = ["#4A90D9", "#F5A623", "#7CB342", "#AB47BC"]

    axes[0].bar(groups, ctr, color=colors[:len(groups)])
    axes[0].set_title("Столбчатый график")
    axes[0].set_xlabel("Группа")
    axes[0].set_ylabel("CTR, %")
    axes[0].grid(axis="y", alpha=0.25)

    for index, value in enumerate(ctr):
        axes[0].text(index, value, f"{value:.2f}%", ha="center", va="bottom")

    axes[1].plot(groups, ctr, marker="o", linewidth=2, color="#3F7FCC")
    axes[1].set_title("Линейный график")
    axes[1].set_xlabel("Группа")
    axes[1].set_ylabel("CTR, %")
    axes[1].grid(alpha=0.25)

    for index, value in enumerate(ctr):
        axes[1].text(index, value, f"{value:.2f}%", ha="center", va="bottom")

    fig.tight_layout()
    return fig


def create_ab_test_figure(result):
    return create_ctr_figure(result)


def _merge_reference_data(users, events):
    users = users.copy()
    events = events.copy()
    users["user_id"] = users["user_id"].astype(str)
    events["user_id"] = events["user_id"].astype(str)
    events["converted"] = pd.to_numeric(
        events["converted"],
        errors="coerce",
    ).fillna(0)
    return pd.merge(events, users, on="user_id")
