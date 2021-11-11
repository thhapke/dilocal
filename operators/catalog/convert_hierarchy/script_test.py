import sys
import json
from os.path import dirname, join, abspath
proj_dir = join(dirname(dirname(dirname(dirname(abspath(__file__))))))
sys.path.insert(0, proj_dir)

import script
from diadmin.dimockapi.mock_api import mock_api
from diadmin.dimockapi.mock_inport import operator_test

api = mock_api(__file__)     # class instance of mock_api
mock_api.print_send_msg = True  # set class variable for printing api.send

optest = operator_test(__file__)

# config parameter


file = 'License.json'
msg = optest.get_msgfile(file)

script.on_input(msg)

for m in api.msg_list :
    jstr  = json.dumps(m['data'].body,indent=4)
    optest.save_strfile(m['data'].body['name']+'_converted.json',jstr)