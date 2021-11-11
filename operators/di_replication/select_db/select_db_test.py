import sys
from os.path import dirname, join, abspath
from os import getcwd
import logging
logging.basicConfig(level=logging.INFO)

proj_dir = join(dirname(dirname(dirname(dirname(abspath(__file__))))))
sys.path.insert(0, proj_dir)
print('*************')
print('Utils dir: {}'.format(proj_dir))
print('Working directory: {}'.format(getcwd()))
print('Script path: {} - {}'.format(__file__,abspath(__file__)))
print('PYTHONPATH: {}'.format(sys.path))


import select_db
from utils.mock_di_api import mock_api, mock_config
from utils.operator_test import operator_test

import yaml
from hdbcli import dbapi
        
api = mock_api(__file__)     # class instance of mock_api
mock_api.print_send_msg = True  # set class variable for printing api.send

optest = operator_test(abspath(__file__))
# config parameter

msg = api.Message(attributes ={'table_name':'TEST_BADCHARS','schema_name' : 'REPLICATION'},body=[[]])

config_path = optest.get_path('config.yaml')
with open(config_path) as yamls :
    params = yaml.safe_load(yamls)


api.config.hanaConnection['connectionProperties'] = {'additionalHosts': [],
                                                     'host': params['host'],
                                                     'ignoreList': [],
                                                     'password': params['password'],
                                                     'port': params['port'],
                                                     'useProxy': False,
                                                     'useTLS': params['useTLS'],
                                                     'user': params['user'],
                                                     'validateCertificate': False}

api.config.package_size = 100
api.config.output = 'CSV'


### Get number of rows of test table
conProp = api.config.hanaConnection['connectionProperties']
conn = dbapi.connect(address=conProp['host'],
                     port=conProp['port'],
                     user=conProp['user'],
                     password=conProp['password'],
                     encrypt=conProp['useTLS'],
                     sslValidateCertificate=conProp['validateCertificate'])
table = msg.attributes['schema_name'] + '.' + msg.attributes['table_name']

sql = f"SELECT COUNT(*) FROM  {table} "
cursor = conn.cursor()
ret = cursor.execute(sql)
num_rows = cursor.fetchone()[0]
cursor.close()
conn.close()

################
# Call Operator
################
count=0
for call in range(0,num_rows,api.config.package_size) :
    select_db.on_input(msg)
    count += 1
    print(f"call: {count}")

################
# Collect Data
###############
if api.config.output == 'JSON':
    output_file = optest.get_path('output.json')
else:
    output_file = optest.get_path('output.csv')
with open(output_file,'w') as outputf :
    for mt in mock_api.msg_list :
        if mt['port'] == 'output':
            outputf.writelines(mt['data'].body)

################
# RESET DB Table
################
sql = f"UPDATE {table} SET \"DIREPL_STATUS\" = \'W\' "
print("*********************************")
print(f'DB Table {table} reset: {sql}')
conn = dbapi.connect(address=conProp['host'],
                     port=conProp['port'],
                     user=conProp['user'],
                     password=conProp['password'],
                     encrypt=conProp['useTLS'],
                     sslValidateCertificate=conProp['validateCertificate'])
cursor = conn.cursor()
ret = cursor.execute(sql)
cursor.close()
conn.close()