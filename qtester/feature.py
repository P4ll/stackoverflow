import pandas as pd
from abc import ABC, abstractmethod, abstractproperty, ABCMeta

class IFeature():
    __metaclass__=ABCMeta

    @abstractproperty
    def name(self):
        """Get name of feature"""

    @abstractmethod
    def get_metric(self, data_row: pd.Series) -> float:
        """Get metric from dataset row"""