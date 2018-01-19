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

def load_without_cold_start(min_games_played=5, min_users_for_game=0):
    steam_df = load_200k()
    # filter users
    return restrict_user_item(steam_df, min_games_played=min_games_played, min_users_for_game=min_users_for_game)

def restrict_user_item(steam_df, min_games_played=5, min_users_for_game=0):
    # filter users
    games_played = steam_df.groupby('uid').count()
    usable_users = games_played[games_played['game_name'] >= min_games_played].reset_index()
    filtered_users = steam_df[steam_df['uid'].isin(usable_users['uid'].values)]
    # filter games
    user_counts = steam_df.groupby('game_name').count()
    usable_games = user_counts[user_counts['playtime'] > min_users_for_game].reset_index()
    return filtered_users[steam_df['game_name'].isin(usable_games['game_name'].values)]
