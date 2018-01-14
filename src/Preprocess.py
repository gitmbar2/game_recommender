import numpy as np
import pandas as pd
import random

class SubsetALSPreprocessor(object):
    def __init__(self, df):
        self.df = df.copy()

    def _rank_playtime(self, time):
        if time <= 1:
            return 0
        if time > 1 and time <= 5:
            return 1
        if time > 6 and time <= 25:
            return 2
        return 3

    def _min_max(self, row):
        # TODO double check this
        if (row['playtime_max'] == row['playtime_min']):
            return 1.0 / row['game_counts']
        diff = row['playtime_max'] - row['playtime_min']
        return (row['playtime'] - row['playtime_min']) / diff

    def _add_playtime_summaries(self, df, max_rank=3):
        aggs = {'playtime_mean': np.mean, 'playtime_min': np.min, 'playtime_max': np.max, 'game_counts': 'count'}
        grouped_means = df.groupby('game_name').agg({'playtime': aggs})
        grouped_means.columns = [col[1] for col in grouped_means.columns]
        joined = df.join(grouped_means, on='game_name')
        joined['playtime_min_max'] = joined.apply(lambda x: self._min_max(x) * max_rank, axis=1)
        return joined

    def _create_uids(self, df, from_column='game_name', to_column='game_uid'):
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

    def get_df(self):
        return self.df

    def process_general(self):
        self.df = self._create_uids(self.df, from_column='game_name', to_column='game_uid')
        return self.df

    def process_buckets(self):
        self.df["playtime_rank"] = self.df['playtime'].map(lambda value: self._rank_playtime(value))
        return self.df

    def process_min_max(self, max_rank=3):
        self.df = self._add_playtime_summaries(self.df, max_rank=max_rank)
        return self.df

    def keep_columns(self, keep_columns):
        existing_columns = set(self.df.columns)
        intersection = existing_columns.intersection(set(keep_columns))
        self.df = self.df[list(intersection)]
        return self.df
