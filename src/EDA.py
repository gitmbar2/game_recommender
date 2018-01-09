import pandas as pd

def load_200k():
    steam_200k_df = pd.read_csv('../data/steam-200k.csv', header=None)
    steam_200k_df.columns = ['uid', 'game_name', 'purchase_action', 'playtime', 'extra']
    steam_200k_df = steam_200k_df.drop('extra', axis=1)
    steam_200k_df = steam_200k_df[steam_200k_df['purchase_action'] == 'play']
    return steam_200k_df

def load_200k_n_games_played(n):
    steam_df = load_200k()
    game_counts = steam_df.groupby('uid').count()
    usable_users = game_counts[game_counts['game_name'] >= 5].reset_index()
    return steam_df[steam_df['uid'].isin(usable_users['uid'].values)]

def rank_playtime(time):
    if time <= 1:
        return 0
    if time > 1 and time <= 5:
        return 1
    if time > 6 and time <= 25:
        return 2
    return 3
