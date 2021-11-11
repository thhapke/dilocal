import trainingdata
from utils.mock_di_api import mock_api
from utils.operator_test import operator_test
        
api = mock_api(__file__)     # class instance of mock_api
mock_api.print_send_msg = True  # set class variable for printing api.send

optest = operator_test(__file__)
# config parameter 
api.config.schema = 'DATAONBOARDING#DATAINTELLIGENCE'    # datatype : string
api.config.tables = ['CYCLING_OUTDOOR','CYCLING_INDOOR','RUNNING','SWIMMING_POOL','SWIMMING_OPEN_WATER']    # datatype : array
api.config.from_year = 2015   # datatype : integer
api.config.to_year = 2021   # datatype : integer


trainingdata.gen()
# print result list
for mt in mock_api.msg_list :
  print('Port: {}'.format(mt['port']))
  print('Data: {}'.format(mt['data']))
  #print(optest.msgtable2df(mt['data']))  
  