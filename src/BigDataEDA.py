import numpy as np
import pandas as pd
import random

big_dataset_path = '../data/steam-800k.jsonl'

def load_big():
    steam_big_df = pd.read_json(big_dataset_path, orient='values', lines=True)
    steam_big_df.columns = ['uid', 'game_id', 'playtime']
    return steam_big_df

def load_big_restrict_data(min_games_played=5, min_users_for_game=0):
    steam_df = load_big()
    # filter users and games
    return get_filtered_user_item(steam_df, min_games_played=min_games_played, min_users_for_game=min_users_for_game)

def get_users_with_min_games(df, min_games_played=5):
    games_counts_df = df.groupby('uid').count()
    usable_users = games_counts_df[games_counts_df['game_uid'] >= min_games_played].reset_index()
    return df[df['uid'].isin(usable_users['uid'].values)]

def get_games_with_min_users(df, min_users_for_game=0):
    user_counts_df = df.groupby('game_uid').count()
    usable_games = user_counts_df[user_counts_df['playtime'] > min_users_for_game].reset_index()
    return df[df['game_uid'].isin(usable_games['game_uid'].values)]

def get_filtered_user_item(steam_df, min_games_played=5, min_users_for_game=0):
    filtered_users_df = get_users_with_min_games(steam_df, min_games_played=min_games_played)
    # filter games
    return get_games_with_min_users(filtered_users_df, min_users_for_game=min_users_for_game)
