import script
from archive.utils.mock_di_api import mock_api
from archive.utils.operator_test import operator_test
        
api = mock_api(__file__)     # class instance of mock_api
mock_api.print_send_msg = True  # set class variable for printing api.send

optest = operator_test(__file__)
# config parameter 


msg = optest.get_file('test_file.csv')
script.on_input(msg)

  