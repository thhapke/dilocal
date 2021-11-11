# Mock apis needs to be commented before used within SAP Data Intelligence
from diadmin.dimockapi.mock_api import mock_api
api = mock_api(__file__)

import copy
import pandas as pd

def on_input(msg):

    header = [item['Name'] for item in msg.attributes['ABAP']['Fields']]
    columns_str = ','.join(header)
    body = columns_str + '\n' + msg.body

    att = copy.deepcopy(msg.attributes)
    att['file'] = {"connection":{"configurationType":"Connection Management","connectionID":"S3"},
                   "path":"/shared","size":0}
    att['filename'] = api.config.cds_view

    msg_output = api.Message(attributes=att,body=body)
    api.send('output',msg_output)  # data type: message.file


api.set_port_callback(['input'],on_input)