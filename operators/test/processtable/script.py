# First 3 lines generated by di-pyoperator - DO NOT CHANGE (Deleted again when uploaded.)
from utils.mock_di_api import mock_api
api = mock_api(__file__)

import pandas as pd
import copy
import io
import os


def on_input1(msg) :

    # Due to input-format PROPOSED transformation into DataFrame
    header = [c['name'] for c in msg.attributes['table']['columns']]
    df = pd.DataFrame(msg.body, columns=header)

    # config parameter 
    #api.config.table_name = None   # datatype : string
    #api.config.size = null   # datatype : integer



    # Sending to outport output1
    # Due to output-format PROPOSED transformation into message.table
    #df.columns = map(str.upper, df.columns)  # for saving to DB upper case is usual
    columns = []
    for col in df.columns : 
        columns.append({"class": str(df[col].dtype),'name': col})
    att = {'table':{'columns':columns,'name':'TABLE','version':1}}
    out_msg = api.Message(attributes=att, body= df.values.tolist())
    api.send('output1',out_msg)    # datatype: message.table


    # Sending to outport output2
    csv = df.to_csv(index=False)
    att = dict(msg.attributes)
    att['file'] = {"connection": {"configurationType": "Connection Management", "connectionID": "DI_DATA_LAKE" },\
                   "path": "/shared/data.csv", "size": 1}
              
    out_msg = api.Message(attributes=att,body=csv)
    api.send('output2',out_msg)    # datatype: message.file


    # Sending to outport output3
    att = dict(msg.attributes)
    out_msg = api.Message(attributes=att,body=None)
    api.send('output3',out_msg)    # datatype: message

api.set_port_callback('input1',on_input1)   # datatype: message.table

def on_input2(msg) :

    # Due to input-format PROPOSED transformation into DataFrame
    df = pd.read_csv(io.BytesIO(msg.body))

    # config parameter 
    #api.config.table_name = None   # datatype : string
    #api.config.size = null   # datatype : integer



    # Sending to outport output1
    # Due to output-format PROPOSED transformation into message.table
    #df.columns = map(str.upper, df.columns)  # for saving to DB upper case is usual
    columns = []
    for col in df.columns : 
        columns.append({"class": str(df[col].dtype),'name': col})
    att = {'table':{'columns':columns,'name':'TABLE','version':1}}
    out_msg = api.Message(attributes=att, body= df.values.tolist())
    api.send('output1',out_msg)    # datatype: message.table


    # Sending to outport output2
    csv = df.to_csv(index=False)
    att = dict(msg.attributes)
    att['file'] = {"connection": {"configurationType": "Connection Management", "connectionID": "DI_DATA_LAKE" },\
                   "path": "/shared/data.csv", "size": 1}
              
    out_msg = api.Message(attributes=att,body=csv)
    api.send('output2',out_msg)    # datatype: message.file


    # Sending to outport output3
    att = dict(msg.attributes)
    out_msg = api.Message(attributes=att,body=None)
    api.send('output3',out_msg)    # datatype: message

api.set_port_callback('input2',on_input2)   # datatype: message.file

def on_input3(msg) :

    # Assumingly the message.body is of type DataFrame
    df = msg.body

    # config parameter 
    #api.config.table_name = None   # datatype : string
    #api.config.size = null   # datatype : integer



    # Sending to outport output1
    # Due to output-format PROPOSED transformation into message.table
    #df.columns = map(str.upper, df.columns)  # for saving to DB upper case is usual
    columns = []
    for col in df.columns : 
        columns.append({"class": str(df[col].dtype),'name': col})
    att = {'table':{'columns':columns,'name':'TABLE','version':1}}
    out_msg = api.Message(attributes=att, body= df.values.tolist())
    api.send('output1',out_msg)    # datatype: message.table


    # Sending to outport output2
    csv = df.to_csv(index=False)
    att = dict(msg.attributes)
    att['file'] = {"connection": {"configurationType": "Connection Management", "connectionID": "DI_DATA_LAKE" },\
                   "path": "/shared/data.csv", "size": 1}
              
    out_msg = api.Message(attributes=att,body=csv)
    api.send('output2',out_msg)    # datatype: message.file


    # Sending to outport output3
    att = dict(msg.attributes)
    out_msg = api.Message(attributes=att,body=None)
    api.send('output3',out_msg)    # datatype: message

api.set_port_callback('input3',on_input3)   # datatype: message
