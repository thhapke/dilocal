# Mock apis needs to be commented before used within SAP Data Intelligence
from diadmin.dimockapi.mock_api import mock_api
api = mock_api(__file__)


import copy
import pandas as pd
import io


def on_input(msg):

    ### INPUT templates
    # Input message.file to DataFrame
    #df = pd.read_csv(io.BytesIO(msg.body))
    
    # Input message.table to DataFrame
    #header = [c['name'] for c in msg.attributes['table']['columns']]
    #df = pd.DataFrame(msg.body, columns=header)
    
    # Input table to DataFrame
    #df = pd.DataFrame(msg.body, columns=msg.attributes['header'])

    data = None

    ### OUTPUT templates
    # Output DataFrame to message.table
    #dtype_map = {'int64':'integer','float64':'float','object':'string','datetime64[ns]':'timestamp'}
    #col_types = { col:dtype_map[dt.name] for col,dt in df.dtypes.items() }
    #table_dict = {'version':1,'columns':list(),'name':'table'}
    #table_dict['columns'] = [{'name':col,'class': col_types[col].lower()} for col in df.columns ]
    #att['table'] = table_dict
    #data = df.values.tolist()
    att = copy.deepcopy(msg.attributes)
    msg_output = api.Message(attributes=att,body=data)
    api.send('output',msg_output)  # data type: message.file


api.set_port_callback(['input'],on_input)