import pandas as pd
from abc import ABC, abstractmethod, abstractproperty, ABCMeta

class IFeature():
    __metaclass__=ABCMeta
    work_mode = "scalar"

    @abstractproperty
    def name(self):
        """Get name of feature"""

    @abstractproperty
    def mode(self):
        """Get work mode"""

    @abstractmethod
    def get_metric(self, data_row: pd.Series) -> float:
        """Get metric from dataset row"""