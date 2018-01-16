import numpy as np
import pandas as pd
import random

class PandasTrainTest(object):
    '''
    '''
    def __init__(self, df, seed=None):
        self.df = df
        if (seed):
            random.seed(seed)

    def _user_games_split(self, test_df, game_split_train=.5):
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
    def _train_test_split_impl(
        self,
        df,
        user_column='uid',
        user_split_train=.8,
        game_split_train=.5,
    ):
        unique_users = df[user_column].unique()
        random.shuffle(unique_users)
        train_users = unique_users[:int((len(unique_users) + 1) * user_split_train)]
        test_users = unique_users[int((len(unique_users) + 1) * user_split_train):]
        train_df = df[df[user_column].isin(train_users)]
        test_df = df[df[user_column].isin(test_users)]
        # append test user training games to train users
        train_games_df, test_games_df = self._user_games_split(test_df, game_split_train=game_split_train)
        final_train_df = train_df.append(train_games_df)
        return (final_train_df, test_games_df)

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
        print('User column is: ', user_column)
        return self._train_test_split_impl(
            self.df,
            user_column=user_column,
            user_split_train=user_split_train,
            game_split_train=game_split_train
        )

    def get_k_folds():
        pass

class SparkTestTrain(object):
    '''
    '''
    def __init__():
        pass
