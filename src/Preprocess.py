import numpy as np
import pandas as pd
import random

class PandasALSPreprocessor(object):
    '''
        For use with data loaded into pandas with specific columns.
        All standard preprocessing before splitting data into training and test sets
        and putting into ALS is done in this class.
        Requires the columns uid, playtime, game_name.
    '''
    def __init__(self, df):
        self.df = df.copy()
        self.standard_columns = ['uid', 'game_uid', 'game_name', 'playtime', 'playtime_min_max']

    def _rank_playtime(self, time):
        if time <= 1:
            return 0
        if time > 1 and time <= 5:
            return 1
        if time > 6 and time <= 25:
            return 2
        return 3

    def _calculate_min_max(self, row):
        # avoid dividing by 0
        if (row['playtime_max'] == row['playtime_min']):
            return 1.0 / row['game_counts']
        diff = row['playtime_max'] - row['playtime_min']
        return (row['playtime'] - row['playtime_min']) / diff

    def _add_playtime_summaries(self, df, max_rank=3):
        '''
            Adds aggregations stats as well as the playtime_min_max fields to a
            pandas DataFrame.
        '''
        aggs = {'playtime_mean': np.mean, 'playtime_min': np.min, 'playtime_max': np.max, 'game_counts': 'count'}
        grouped_means = df.groupby('game_name').agg({'playtime': aggs})
        grouped_means.columns = [col[1] for col in grouped_means.columns]
        joined = df.join(grouped_means, on='game_name')
        joined['playtime_min_max'] = joined.apply(lambda x: (self._calculate_min_max(x) * max_rank), axis=1)
        return joined

    def _create_uids(self, df, from_column='game_name', to_column='game_uid'):
        '''
            If the ALS algorithm requires ids for items instead of names,
            this will ensure that each item has a unique id.
        '''
        uid = 0
        uid_map = {}
        for item in df[from_column]:
            if item in uid_map:
                continue
            uid_map[item] = uid
            uid += 1
        df[to_column] = df[from_column].map(lambda name: uid_map[name])
        return df

    def get_df(self):
        return self.df

    def add_item_ids(self):
        self.df = self._create_uids(self.df, from_column='game_name', to_column='game_uid')
        return self.df

    def add_rank_buckets(self):
        self.df["playtime_rank"] = self.df['playtime'].map(lambda value: self._rank_playtime(value))
        return self.df

    def add_min_max(self, max_rank=3):
        self.df = self._add_playtime_summaries(self.df, max_rank=max_rank)
        return self.df

    def keep_columns(self, keep_columns):
        existing_columns = set(self.df.columns)
        intersection = existing_columns.intersection(set(keep_columns))
        self.df = self.df[list(intersection)]
        return self.df

    def keep_standard_columns(self):
        self.keep_columns(self.standard_columns)
        return self.df
