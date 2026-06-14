import pandas as pd


def run_ctr_analysis(csv_path):
    raw = pd.read_csv(csv_path)
    cleaned, quality = clean_ctr_data(raw)
    metrics = calculate_group_metrics(cleaned)

    result = {
        "csv_path": csv_path,
        "raw": raw,
        "cleaned": cleaned,
        "quality": quality,
        "metrics": metrics,
    }
    result["text"] = format_ctr_result(result)
    return result


def run_full_ab_test(csv_path):
    return run_ctr_analysis(csv_path)


def clean_ctr_data(df):
    before_rows = len(df)
    duplicate_count = int(df["user_id"].duplicated().sum())

    cleaned = df.drop_duplicates(subset="user_id", keep="first").copy()
    cleaned["converted"] = pd.to_numeric(
        cleaned["converted"],
        errors="coerce",
    ).fillna(0)
    cleaned["converted"] = cleaned["converted"].astype(int)

    expected_page = {
        "control": "old_page",
        "treatment": "new_page",
    }
    valid_mask = cleaned.apply(
        lambda row: expected_page.get(row["group"]) == row["landing_page"],
        axis=1,
    )
    mismatch_count = int((~valid_mask).sum())
    cleaned = cleaned.loc[valid_mask].copy()

    quality = {
        "before_rows": before_rows,
        "duplicate_count": duplicate_count,
        "mismatch_count": mismatch_count,
        "after_rows": len(cleaned),
    }
    return cleaned, quality


def calculate_group_metrics(cleaned):
    metrics = cleaned.groupby("group").agg(
        users=("user_id", "count"),
        clicks=("converted", "sum"),
    )
    metrics["ctr"] = metrics["clicks"] / metrics["users"]
    return metrics.sort_index()


def calculate_ctr_stats(users, events):
    users = users.copy()
    events = events.copy()
    users["user_id"] = users["user_id"].astype(str)
    events["user_id"] = events["user_id"].astype(str)
    events["converted"] = pd.to_numeric(
        events["converted"],
        errors="coerce",
    ).fillna(0)

    df = pd.merge(events, users, on="user_id")
    stats = df.groupby("group").agg(
        impressions=("user_id", "count"),
        clicks=("converted", "sum"),
    )
    stats["ctr_percent"] = (stats["clicks"] / stats["impressions"]) * 100
    return stats


def compare_ctr(stats):
    if len(stats) < 2:
        return "Недостаточно групп для сравнения CTR."

    best_group = stats["ctr_percent"].idxmax()
    worst_group = stats["ctr_percent"].idxmin()
    difference = (
        stats.loc[best_group, "ctr_percent"]
        - stats.loc[worst_group, "ctr_percent"]
    )

    return (
        f"Группа с большим CTR: {best_group}. "
        f"Разница с группой {worst_group}: {difference:.2f} п.п."
    )


def format_ctr_result(result):
    metrics = result["metrics"]
    quality = result["quality"]

    lines = [
        "CTR ПО ГРУППАМ",
        f"Строк в файле: {quality['before_rows']}",
        f"Удалено дублей user_id: {quality['duplicate_count']}",
        f"Удалено ошибок group/page: {quality['mismatch_count']}",
        f"Строк в расчете: {quality['after_rows']}",
        "",
    ]

    for group, row in metrics.iterrows():
        lines.append(
            f"{group}: показы = {int(row['users'])}, "
            f"клики = {int(row['clicks'])}, "
            f"CTR = {row['ctr'] * 100:.2f}%"
        )

    if len(metrics) >= 2:
        best_group = metrics["ctr"].idxmax()
        worst_group = metrics["ctr"].idxmin()
        difference = (
            metrics.loc[best_group, "ctr"]
            - metrics.loc[worst_group, "ctr"]
        ) * 100
        lines.extend([
            "",
            f"Лучший CTR у группы {best_group}.",
            f"Разница с группой {worst_group}: {difference:.2f} п.п.",
        ])

    return "\n".join(lines)
