import pandas as pd
import numpy as np

a = [1, 2, 3]
b = [4, 5, 7]

zz = pd.DataFrame()
zz['a'] = a
zz['b'] = b
print(zz[:2])