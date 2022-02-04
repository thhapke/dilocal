import trainingbestinterval
from utils.mock_di_api import mock_api
from utils.operator_test import operator_test


import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
        
api = mock_api(__file__)     # class instance of mock_api
mock_api.print_send_msg = False  # set class variable for printing api.send

optest = operator_test(__file__)
# config parameter 
api.config.interval_width = 10   # datatype : integer
api.config.min_periods = 10   # datatype : integer

msg = optest.get_msgtable('RUNNING.csv')
trainingbestinterval.on_input(msg)
# print result list
dflist = list()
for mt in mock_api.msg_list :
  dflist.append(optest.msgtable2df(mt['data']))

df = pd.concat(dflist)
print(df)
