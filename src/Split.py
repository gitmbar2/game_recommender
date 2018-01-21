import numpy as np
import pandas as pd
import random
from functools import reduce

class PandasTrainTest(object):
    '''
    '''
    def __init__(self, df, seed=None):
        self.df = df
        if (seed):
            random.seed(seed)

    def user_games_split(self, test_df, game_split_train=.5):
        train_indices = []
        test_indices = []
        # can do uid in users and game in gameid
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

    def _get_unique_users(self, df, user_column='uid'):
        unique_users = df[user_column].unique()
        random.shuffle(unique_users)
        return unique_users

    def user_only_split(self, user_column='uid', user_split_train=.8):
        df = self.df
        unique_users = self._get_unique_users(df, user_column)
        train_users = unique_users[:int((len(unique_users) + 1) * user_split_train)]
        test_users = unique_users[int((len(unique_users) + 1) * user_split_train):]
        train_df = df[df[user_column].isin(train_users)]
        test_df = df[df[user_column].isin(test_users)]
        return (train_df, test_df)

    # Consider sampling with replacement?  What does that mean in rec
    def train_test_split(
        self,
        user_column='uid',
        user_split_train=.8,
        game_split_train=.5,
    ):
        '''
            Custom train test split for recommender.
            Puts n percent of users into train and 1-n into test.
            For each user in test, put half of their games back into train
        '''
        train_df, test_df = self.user_only_split(user_column, user_split_train)
        # append test user training games to train users
        train_games_df, test_games_df = self.user_games_split(test_df, game_split_train=game_split_train)
        final_train_df = train_df.append(train_games_df)
        return (final_train_df, test_games_df)

    def get_k_folds(self, k, user_column='uid', game_split_train=.5):
        unique_users = self._get_unique_users(self.df)
        print('Number of users: ', len(unique_users))
        len_over_k = int((len(unique_users) + 1) / k)
        user_divisions = []
        for i in range(0, k):
            user_subset = unique_users[i * len_over_k : (i + 1) * len_over_k]
            user_divisions.append(user_subset)
        # return user_divisions
        # just do range
        finals = []
        for i in range(0, len(user_divisions)):
            k_test_ids = user_divisions[i]
            k_train = user_divisions[0:i] + user_divisions[i+1:]
            k_train_ids = [item for sublist in k_train for item in sublist]
            k_test_df = self.df[self.df[user_column].isin(k_test_ids)]
            k_train_df = self.df[self.df[user_column].isin(k_train_ids)]
            k_train_games_df, k_test_games_df = self.user_games_split(k_test_df, game_split_train=game_split_train)
            final_k_train_df = k_train_df.append(k_train_games_df)
            finals.append((final_k_train_df, k_test_games_df))
        return finals

    def run_k_folds(self, model, evaluator):
        # get k folds
        # run function on each split
        # evaluate
        # return average loss
        pass

class SparkTrainTest(object):
    '''
    '''
    def __init__(self):
        pass
