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

    def _get_unique_users(self, df, user_column='uid'):
        # we dont want to change the dataset
        unique_users = df[user_column].unique()
        random.shuffle(unique_users)
        return unique_users

    def user_only_split(self, user_column='uid', user_split_train=.8):
        '''
            splits data into different groups based on uid
            user_split_train decides group sizes (of percent p, 1-p)
        '''
        df = self.df
        # if we didnt care about grouping users, random index
        unique_users = self._get_unique_users(df, user_column)
        cutoff = int((len(unique_users) + 1) * user_split_train)
        train_users = unique_users[:cutoff]
        test_users = unique_users[cutoff:]
        # isin uses set under the hood
        train_df = df[df[user_column].isin(train_users)]
        test_df = df[df[user_column].isin(test_users)]
        return (train_df, test_df)

    def user_games_split(self, test_df, game_split_train=.5):
        train_indices = []
        test_indices = []
        # for every user, add n*p games to train and n*(p-1) to test
        for uid in test_df['uid'].unique():
            user_data = test_df[test_df['uid'] == uid]
            indices = user_data.index.values
            random.shuffle(indices)
            cutoff = int((len(indices) + 1) * game_split_train)
            train_game_indices = indices[:cutoff]
            test_game_indices = indices[cutoff:]
            train_indices += train_game_indices.tolist()
            test_indices += test_game_indices.tolist()
        train_games = test_df.loc[train_indices,:]
        test_games = test_df.loc[test_indices,:]
        return (train_games, test_games)

    def train_test_split(
        self,
        user_column='uid',
        user_split_train=.8,
        game_split_train=.5,
    ):
        '''
            Custom train test split for recommender.
            Puts p percent of users into train and 1-p into test.
            For each user in test, put half of their games back into train
        '''
        train_df, test_df = self.user_only_split(user_column, user_split_train)
        # append test user training games to train users
        train_games_df, test_games_df = self.user_games_split(test_df, game_split_train=game_split_train)
        final_train_df = train_df.append(train_games_df)
        return (final_train_df, test_games_df)

    def _kth_train_test(self, user_divisions, k, user_column, game_split_train):
        k_test_ids = user_divisions[k]
        k_train_ids = []
        # more efficient than map and flatten
        for i in range(len(user_divisions)):
            if i is not k:
                k_train_ids += user_divisions[i]
        # maybe, for row in df, if in k_train append to k_train else append to test
        k_train_df = self.df[self.df[user_column].isin(k_train_ids)]
        k_test_df = self.df[self.df[user_column].isin(k_test_ids)]
        k_train_games_df, k_test_games_df = self.user_games_split(k_test_df, game_split_train=game_split_train)
        final_k_train_df = k_train_df.append(k_train_games_df)
        return (final_k_train_df, k_test_games_df)

    def get_k_folds(self, k, user_column='uid', game_split_train=.5):
        """
            game_split_train is the percent of games in the training set for test users
        """
        unique_users = self._get_unique_users(self.df).tolist()
        len_over_k = int((len(unique_users) + 1) / k)
        # divide users into k groups with equal number of users (not equal rows)
        user_divisions = [unique_users[i * len_over_k : (i + 1) * len_over_k] for i in range(0, k)]
        # create train/test splits for each group
        finals = []
        for k in range(0, len(user_divisions)):
            finals.append(self._kth_train_test(
                user_divisions,
                k,
                user_column,
                game_split_train
            ))
        return finals


class SparkTrainTest(object):
    '''
    '''
    def __init__(self):
        pass
