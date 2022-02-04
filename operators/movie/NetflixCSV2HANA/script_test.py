import script
from archive.utils.mock_di_api import mock_api
from archive.utils.operator_test import operator_test
        
api = mock_api(__file__)     # class instance of mock_api
mock_api.print_send_msg = True  # set class variable for printing api.send

optest = operator_test(__file__)

# config parameter 
api.config.type = '*'    # datatype : string
data0 = optest.get_file('test_file0.csv')

msg = api.Message(attributes={'operator':'movie.NetflixCSV2HANA'},body = data0)
script.on_input(msg)
# print result list
for mt in mock_api.msg_list :
  print('Port: {}'.format(mt['port']))
  print('Data: {}'.format(mt['data']))
  #print(optest.msgtable2df(mt['data']))  
  