import pandas as pd

#Расчет CTR = (clicks / impressions) * 100%
def calculate_ctr_stats(users, events):

    df = pd.merge(events, users, on='user_id')
    stats = df.groupby('group').agg(
        impressions=('user_id', 'count'),
        clicks=('converted', 'sum')
    )
    stats['ctr_percent'] = (stats['clicks'] / stats['impressions']) * 100
    return stats
