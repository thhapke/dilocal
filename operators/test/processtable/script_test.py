import script
from utils.mock_di_api import mock_api
from utils.operator_test import operator_test
        
api = mock_api(__file__)     # class instance of mock_api
mock_api.print_send_msg = True  # set class variable for printing api.send

optest = operator_test(__file__)
# config parameter 
api.config.table_name = None   # datatype : string
api.config.size = null   # datatype : integer


msg = optest.get_msgtable('testdata.csv')
script.on_input1(msg)
msg1 = optest.get_file('test_file1.csv')
script.on_input2(msg1)
msg2 = api.Message(attributes={'operator':'test.processtable'},body = None)
script.on_input3(msg2)
# print result list
for mt in mock_api.msg_list :
  print('*********************')
  print('Port: {}'.format(mt['port']))
  print('Attributes: {}'.format(mt['data'].attributes))
  print('Data: {}'.format(mt['data'].body))
  #print(optest.msgtable2df(mt['data']))  
  