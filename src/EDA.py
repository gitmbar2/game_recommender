import numpy as np
import pandas as pd
import random

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

def user_games_split(test_df, game_split_train=.5, seed=None):
    if (seed):
        random.seed(seed)
    train_indices = []
    test_indices = []
    for uid in test_df['uid'].unique():
        user_data = test_df[test_df['uid'] == uid]
        indices = user_data.index.values
        random.shuffle(indices)
        train_game_indices = indices[:int((len(indices) + 1) * game_split_train)]
        test_game_indices = indices[int((len(indices) + 1) * game_split_train):]
        train_indices += train_game_indices.tolist()
        test_indices += test_game_indices.tolist()
    train_games = test_df.loc[train_indices,:]
    test_games = test_df.loc[test_indices,:]
    return (train_games, test_games)

# Consider sampling with replacement?  What does that mean in rec
def recommender_train_test_split(
    df,
    user_column='uid',
    user_split_train=.8,
    game_split_train=.75,
    seed=None
):
    '''
        Custom train test split for recommender.
        Puts n percent of users into train and 1-n into test.
        For each user in test, put half of their games back into train
    '''
    if (seed):
        random.seed(seed)
    unique_users = df[user_column].unique()
    random.shuffle(unique_users)
    train_users = unique_users[:int((len(unique_users) + 1) * user_split_train)]
    test_users = unique_users[int((len(unique_users) + 1) * user_split_train):]
    train_df = df[df[user_column].isin(train_users)]
    test_df = df[df[user_column].isin(test_users)]
    # append test user training games to train users
    train_games_df, test_games_df = user_games_split(test_df, game_split_train=game_split_train, seed=seed)
    final_train_df = train_df.append(train_games_df)
    return (final_train_df, test_games_df)


def get_uids(df, from_column='game_name', to_column='game_uid'):
    # fitting ALS must have numbers for itemCol and userCol
    uid = 0
    uid_map = {}
    for item in df[from_column]:
        if item in uid_map:
            continue
        uid_map[item] = uid
        uid += 1
    df[to_column] = df[from_column].map(lambda name: uid_map[name])
    return df
