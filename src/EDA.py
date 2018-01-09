import numpy as np
import pandas as pd

def load_200k():
    steam_200k_df = pd.read_csv('../data/steam-200k.csv', header=None)
    steam_200k_df.columns = ['uid', 'game_name', 'purchase_action', 'playtime', 'extra']
    steam_200k_df = steam_200k_df.drop('extra', axis=1)
    steam_200k_df = steam_200k_df[steam_200k_df['purchase_action'] == 'play']
    return steam_200k_df

def load_without_cold_start(min_games=5, min_users=0):
    steam_df = load_200k()
    # filter users
    game_counts = steam_df.groupby('uid').count()
    usable_users = game_counts[game_counts['game_name'] >= min_games].reset_index()
    filtered_users = steam_df[steam_df['uid'].isin(usable_users['uid'].values)]
    # filter games
    user_counts = steam_df.groupby('game_name').count()
    usable_games = user_counts[user_counts['playtime'] > min_users].reset_index()
    return filtered_users[steam_df['game_name'].isin(usable_games['game_name'].values)]

def rank_playtime(time):
    if time <= 1:
        return 0
    if time > 1 and time <= 5:
        return 1
    if time > 6 and time <= 25:
        return 2
    return 3

def add_summaries(df, max_rank=3):
    # Do min-max normalization
    def min_max(row):
        # TODO double check this
        if (row['playtime_max'] == row['playtime_min']):
            return 1.0 / row['game_counts']
        diff = row['playtime_max'] - row['playtime_min']
        return (row['playtime'] - row['playtime_min']) / diff

    aggs = {'playtime_mean': np.mean, 'playtime_min': np.min, 'playtime_max': np.max, 'game_counts': 'count'}
    grouped_means = df.groupby('game_name').agg({'playtime': aggs})
    grouped_means.columns = [col[1] for col in grouped_means.columns]
    joined = df.join(grouped_means, on='game_name')
    joined['min_max'] = joined.apply(lambda x: min_max(x) * max_rank, axis=1)
    return joined
