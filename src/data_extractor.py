import pandas as pd
from abc import ABC, abstractmethod, abstractproperty, ABCMeta
import sys
sys.path.append('get_data_pipeline')
from get_data_pipeline.get_init_data import get_all_data
from get_data_pipeline.get_user_data import save_add_user_info
from get_data_pipeline.add_user_data import insert_user_data
from datetime import date, timedelta


class IDataExtractor():
    __metaclass__=ABCMeta

    @abstractmethod
    def get_data(self, *args, **kwargs) -> pd.DataFrame:
        """Get metric from dataset row"""


class DataExtractor(IDataExtractor):
    def get_data(self, begin_time: date=None, end_time: date=None) -> pd.DataFrame:
        df = get_all_data(begin_time=begin_time, end_time=end_time)
        user_df = save_add_user_info(df)
        insert_user_data(df, user_df)
        return df

if __name__ == '__main__':
    de = DataExtractor()
    de.get_data()