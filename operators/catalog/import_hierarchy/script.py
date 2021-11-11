# Mock apis needs to be commented before used within SAP Data Intelligence
from diadmin.dimockapi.mock_api import mock_api
api = mock_api(__file__)

import copy
import os
from urllib.parse import urljoin


from dimetadata_api.catalog import add_path_id_list, upload_hierarchy

def on_input(msg):

    # Catalogue from file
    hierarchy = msg.body
    if not 'paths' in hierarchy:
        add_path_id_list(hierarchy)

    host = api.config.http_connection['connectionProperties']['host']
    pwd = api.config.http_connection['connectionProperties']['password']
    user = api.config.http_connection['connectionProperties']['user']
    path = api.config.http_connection['connectionProperties']['path']
    tenant = os.environ.get('VSYSTEM_TENANT')
    if not tenant :
        tenant = 'default'

    conn = {'url':urljoin(host,path),'auth':(tenant+'\\'+ user,pwd)}

    upload_hierarchy(conn,hierarchy)

    att = copy.deepcopy(msg.attributes)
    msg_success = api.Message(attributes=att,body=hierarchy)
    api.send('success',msg_success)  # data type: message


api.set_port_callback(['input'],on_input)