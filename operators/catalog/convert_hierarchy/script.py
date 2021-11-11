# Mock apis needs to be commented before used within SAP Data Intelligence
from diadmin.dimockapi.mock_api import mock_api
api = mock_api(__file__)

import json
import io
import copy

def add_dinode(parent_new_node,dinode):
    node = {'name':dinode['tagInfo']['tag']['name'],
            'description':dinode['tagInfo']['tag']['description'],
            'paths':dinode['tagInfo']['tag']['path'],
            'nodes':list()}
    parent_new_node['nodes'].append(node)
    for c in dinode['children'] :
        add_dinode(node,c)

def on_input(msg):

    jfile = json.load(io.BytesIO(msg.body))

    # SAP Data Intelligence Format
    hierarchy = dict()
    if 'hierarchy' in jfile and 'content' in jfile:
        hierarchy['name'] = jfile['hierarchy']['hierarchyDescriptor']['name']
        hierarchy['description'] = jfile['hierarchy']['hierarchyDescriptor']['description']
        hierarchy['nodes'] = list()
        hierarchy['paths'] = ''
        for c in jfile['content'] :
            add_dinode(hierarchy,c)

    elif 'name' in jfile and 'nodes' in jfile and 'description' in jfile :
         hierarchy = jfile
    else:
        raise ImportError('Unknown format')

    att = copy.deepcopy(msg.attributes)
    msg_output = api.Message(attributes=att,body=hierarchy)
    api.send('output',msg_output)  # data type: message


api.set_port_callback(['input'],on_input)