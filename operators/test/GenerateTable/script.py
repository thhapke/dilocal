# First 3 lines generated by di-pyoperator - DO NOT CHANGE (Deleted again when uploaded.)
from utils.mock_di_api import mock_api
api = mock_api(__file__)

import pandas as pd
import copy
import os


def gen() :

    # config parameter 
    #api.config.num_tables = null   # datatype : integer



    # Sending to outport output1
    att = {'operator':'generator'}
    out_msg = api.Message(attributes=att,body=None)

    # Sending to outport output2
    # Due to output-format PROPOSED transformation into message.table
    df = pd.DataFrame(data={'col1': [1, 2], 'col2': ['ab', 'cd']})
    #df.columns = map(str.upper, df.columns)  # for saving to DB upper case is usual
    columns = []
    for col in df.columns : 
        columns.append({"class": str(df[col].dtype),'name': col})
    att = {'operator':'generator','table':{'columns':columns,'name':'TABLE','version':1}}
    out_msg = api.Message(attributes=att, body= df.values.tolist())

    # Sending to outport output3
    csv = df.to_csv(index=False)
    att = {'operator':'generator','file' : {"connection": {"configurationType": "Connection Management", "connectionID": "DI_DATA_LAKE" },\
                   "path": "/shared/data.csv", "size": 1}}
              
    out_msg = api.Message(attributes=att,body=csv)
api.add_generator(gen)