#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:17:34 2020

@author: hamishgibbs
"""

import sys
import requests
import json
import pandas as pd
from datetime import datetime

def main(_args):
    
    current_data = pd.read_csv(_args[len(_args) - 1], index_col = 0)
    
    r = requests.get(_args[1])
    
    j_data = json.loads(r.text)
    
    new_data = pd.DataFrame(j_data['datapoints'])
    new_data = new_data.loc[new_data['name'] == 'one_day', :]
    
    new_data = pd.concat([new_data, current_data]).drop_duplicates()
    
    new_data.to_csv(_args[len(_args) - 1])
    
    print(str(datetime.now()).split('.')[0] + " Success.")
    
if __name__ == "__main__":
    
    _args = sys.argv
    
    main(_args)
