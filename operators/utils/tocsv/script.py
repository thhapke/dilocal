# First 3 lines generated by di-pyoperator - DO NOT CHANGE (Deleted again when uploaded.)
from utils.mock_di_api import mock_api
api = mock_api(__file__)

import pandas as pd
import json
import os


def on_input(msg) :

    # Due to input-format PROPOSED transformation into DataFrame
    header = [c['name'] for c in msg.attributes['table']['columns']]
    df = pd.DataFrame(msg.body, columns=header)

    # config parameter 

    # dump data
    csv = df.to_csv(index=False)
    att = dict(msg.attributes)
    filename = ''
    if not filename and 'table_name' in att  :
        filename = att['table_name'] + '.csv'
    else :
        filename = 'data.csv'
    if not 'file' in att :
        connectionID = "DI_DATA_LAKE"
        path = os.path.join('/shared/',filename)
        att['file'] = {"connection": {"configurationType": "Connection Management", "connectionID": connectionID },\
                       "path": path, "size": 1}
        att['filename'] = filename
              
    data_msg = api.Message(attributes=att,body=csv)
    api.send('output',data_msg)    # datatype: message.file

    # dump attributes
    atta = dict(att)
    att_filename = filename.split('.')[0] + '_attributes.json'
    atta['file']['path'] = os.path.join('/shared/', att_filename)
    atta['filename'] = att_filename
    att_msg = api.Message(attributes=atta,body=json.dumps(atta))
    api.send('attributes',att_msg)    # datatype: message.file

api.set_port_callback('input',on_input)   # datatype: message.table
