import numpy as np
import pandas as pd
import random

def load_200k():
    steam_200k_df = pd.read_csv('../data/steam-200k.csv', header=None)
    steam_200k_df.columns = ['uid', 'game_name', 'purchase_action', 'playtime', 'extra']
    steam_200k_df = steam_200k_df.drop('extra', axis=1)
    steam_200k_df = steam_200k_df[steam_200k_df['purchase_action'] == 'play']
    steam_200k_df = steam_200k_df.drop('purchase_action', axis=1)
    return steam_200k_df

def load_200k_restrict_data(min_games_played=5, min_users_for_game=0):
    steam_df = load_200k()
    # filter users and games
    return get_filtered_user_item(steam_df, min_games_played=min_games_played, min_users_for_game=min_users_for_game)

def get_users_with_min_games(df, min_games_played=5):
    games_counts_df = df.groupby('uid').count()
    usable_users = games_counts_df[games_counts_df['game_name'] >= min_games_played].reset_index()
    return df[df['uid'].isin(usable_users['uid'].values)]

def get_games_with_min_users(df, min_users_for_game=0):
    user_counts_df = df.groupby('game_name').count()
    usable_games = user_counts_df[user_counts_df['playtime'] > min_users_for_game].reset_index()
    return df[df['game_name'].isin(usable_games['game_name'].values)]

def get_filtered_user_item(steam_df, min_games_played=5, min_users_for_game=0):
    filtered_users_df = get_users_with_min_games(steam_df, min_games_played=min_games_played)
    # filter games
    return get_games_with_min_users(filtered_users_df, min_users_for_game=min_users_for_game)
