import script
from archive.utils.mock_di_api import mock_api
from archive.utils.operator_test import operator_test
        
api = mock_api(__file__)     # class instance of mock_api
mock_api.print_send_msg = False  # set class variable for printing api.send

optest = operator_test(__file__)
# config parameter 
api.config.type = '*'    # datatype : string


msg = optest.get_msgfile('netflix_titles_xxl.csv')
script.on_input(msg)
# print result list
for mt in mock_api.msg_list :
  print('*********************')
  print('Port: {}'.format(mt['port']))
  print('Attributes: {}'.format(mt['data'].attributes))
  print('Data: {}'.format(mt['data'].body))
  #print(optest.msgtable2df(mt['data']))  
  