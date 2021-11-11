# Mock apis needs to be commented before used within SAP Data Intelligence
from diadmin.dimockapi.mock_api import mock_api
api = mock_api(__file__)

import json
from urllib.parse import urljoin
from dimetadata_api.catalog import get_hierarchy_names, get_hierarchy_tags
import os

def gen():

    host = api.config.http_connection['connectionProperties']['host']
    pwd = api.config.http_connection['connectionProperties']['password']
    user = api.config.http_connection['connectionProperties']['user']
    path = api.config.http_connection['connectionProperties']['path']
    tenant = os.environ.get('VSYSTEM_TENANT')
    if not tenant :
        tenant = 'default'

    conn = {'url':urljoin(host,path),'auth':(tenant+'\\'+ user,pwd)}

    hnames = get_hierarchy_names(conn, search=api.config.hierarchy)

    hierarchies = list()
    for h in hnames['tagHierarchies'] :
        hierarchies.append(get_hierarchy_tags(conn, h["tagHierarchy"]['id']))

    # to avoid having a list of 1 element
    if len(hierarchies) == 1 :
        jfile = json.dumps(hierarchies[0],indent=4)
    else :
        jfile = json.dumps(hierarchies,indent=4)

    att = {'hierarchy':api.config.hierarchy}
    msg_success = api.Message(attributes=att,body=jfile)
    api.send('output',msg_success)  # data type: message

api.add_generator(gen)