import pandas as pd
import re
# from libs.my_paths import base_final_file, base_optimal_data
import numpy as np  
import matplotlib.pyplot as plt
import numpy as np 
import scipy.stats as stats 
import matplotlib.pyplot as plt
 
class UnnecessaryInformation:
    def get_metric(self, inputText, data: pd.DataFrame) -> bool:
             
        len_of_each = []
        mid_count = 0

        for i, elem in enumerate(data["post_body"]):
            mid_count += len(elem)
            text = re.search('<code>(.|\n)*?<\/code>',elem)
            if text != None:
                len_of_each.append(len(text.group(0)))
            else:
                text = len_of_each.append(0)
        h = len_of_each
        h.sort() 
        hmean = np.mean(h)
        hstd = np.std(h) 
        pdf = stats.norm.pdf(h, hmean, hstd) 
        fit = stats.norm.pdf(h, np.mean(h), np.std(h)) 
        
        right_border = hmean + hstd        
        if(len(inputText) < right_border):
            return 0
        else: 
            return 1
        
    def name(self):
        return "debug_inf"

