#
#  SPDX-FileCopyrightText: 2021 Thorsten Hapke <thorsten.hapke@sap.com>
#
#  SPDX-License-Identifier: Apache-2.0
#

# DI-PYOPERATOR GENERATED - DO NOT CHANGE this line and the following 3 lines (Deleted when uploaded.)
from utils.mock_di_api import mock_api

api = mock_api(__file__)

import copy
from datetime import datetime

import pandas as pd
import numpy as np
from hdbcli import dbapi

typemap = {1: {'hana': 'TINYINT', 'pandas': 'int64'}, 2: {'hana': 'SMALLINT', 'pandas': 'int64'}, 3: {'hana': 'INT', 'pandas': 'int64'},
           4: {'hana': 'BIGINT', 'pandas': 'int64'}, 5: {'hana': 'DECIMAL', 'pandas': 'int64'}, 6: {'hana': 'REAL', 'pandas': 'float64'},
           7: {'hana': 'DOUBLE', 'pandas': 'float64'}, 8: {'hana': 'CHAR', 'pandas': 'object'}, 9: {'hana': 'VARCHAR', 'pandas': 'object'},
           10: {'hana': 'NCHAR', 'pandas': 'object'}, 11: {'hana': 'NVARCHAR', 'pandas': 'object'}, 12: {'hana': 'BINARY', 'pandas': 'object'},
           13: {'hana': 'VARBINARY', 'pandas': 'object'}, 14: {'hana': 'DATE', 'pandas': 'datetime64'}, 15: {'hana': 'TIME', 'pandas': 'datetime64'},
           16: {'hana': 'TIMESTAMP', 'pandas': 'datetime64'}, 25: {'hana': 'CLOB', 'pandas': 'object'}, 26: {'hana': 'NCLOB', 'pandas': 'object'},
           27: {'hana': 'BLOB', 'pandas': 'object'}, 28: {'hana': 'BOOLEAN', 'pandas': 'bool'}, 29: {'hana': 'STRING', 'pandas': 'object'},
           30: {'hana': 'NSTRING', 'pandas': 'object'}, 31: {'hana': 'BLOCATOR', 'pandas': 'object'}, 32: {'hana': 'NLOCATOR', 'pandas': 'object'},
           35: {'hana': 'VARCHAR2', 'pandas': 'object'}, 36: {'hana': 'VARCHAR3', 'pandas': 'object'}, 37: {'hana': 'NVARCHAR3', 'pandas': 'object'},
           38: {'hana': 'VARBINARY3', 'pandas': 'object'}, 47: {'hana': 'SMALLDECIMAL', 'pandas': 'float64'}, 48: {'hana': 'ABAPITAB', 'pandas': 'object'},
           49: {'hana': 'ABAPSTRUCT', 'pandas': 'object'}, 50: {'hana': 'ARRAY', 'pandas': 'object'}, 51: {'hana': 'TEXT', 'pandas': 'object'},
           52: {'hana': 'SHORTTEXT', 'pandas': 'object'}, 55: {'hana': 'ALPHANUM', 'pandas': 'object'}, 61: {'hana': 'LONGDATE', 'pandas': 'datetime64'},
           62: {'hana': 'SECONDDATE', 'pandas': 'datetime64'}, 63: {'hana': 'DAYDATE', 'pandas': 'datetime64'}, 64: {'hana': 'SECONDTIME', 'pandas': 'datetime64'}}

operator_name = 'select_db'

def log(log_str,level='info') :
    if level == 'debug' :
        api.logger.debug(log_str)
    elif level == 'warning':
        api.logger.warning(log_str)
    elif level == 'error':
        api.logger.error(log_str)
    else :
        api.logger.info(log_str)

    now = datetime.now().strftime('%H:%M:%S')
    api.send('log','{} | {} | {} | {}'.format(now,level,operator_name,log_str))


def on_input(msg):

    att = copy.deepcopy(msg.attributes)

    conProp = api.config.hanaConnection['connectionProperties']
    conn = dbapi.connect(address=conProp['host'],
                         port=conProp['port'],
                         user=conProp['user'],
                         password=conProp['password'],
                         encrypt=conProp['useTLS'],
                         sslValidateCertificate=conProp['validateCertificate'])

    table = att['schema_name'] + '.' + att['table_name']

    #
    # Block Data
    #
    att['pid'] = int(datetime.utcnow().timestamp() * 1000000)
    package_size = int(api.config.package_size)

    if package_size > 0:
        sql = 'UPDATE TOP {packagesize} {table} SET \"DIREPL_STATUS\" = \'B\', \"DIREPL_PID\" = {pid} ' \
              'WHERE  \"DIREPL_STATUS\" = \'W\' OR \"DIREPL_STATUS\" IS NULL '.format(packagesize=package_size,
                                                                                      table=table, pid=att['pid'])
    else:
        sql = 'UPDATE {table} SET \"DIREPL_STATUS\" = \'B\', \"DIREPL_PID\" = {pid} ' \
              'WHERE  \"DIREPL_STATUS\" = \'W\' OR \"DIREPL_STATUS\" IS NULL '.format(table=table, pid=att['pid'])
    log(sql)
    cursor = conn.cursor()
    ret = cursor.execute(sql)
    if not ret:
        log('DB connection failed!',level='error')
        return None

    #
    # Select Data
    #
    sql = 'SELECT * FROM {table} WHERE \"DIREPL_PID\" = \'{pid}\' '.\
        format(table=table,pid= att['pid'])
    log('{}'.format(sql))


    try :
        cursor = conn.cursor()
        ret = cursor.execute(sql)
        log('data retrieved')
        if not ret:
            log('DB connection failed!',level='error')
            return None
        rows = cursor.fetchall()
    except :
        log('fails reading data from db')

    columns = []
    colum_names = []
    for col in cursor.description:
        hanadtype = typemap[col[1]]['hana']
        pddtype = typemap[col[1]]['pandas']
        name = col[0]
        columns.append({"class": pddtype, "name": name, "type": {"hana": hanadtype}})
        colum_names.append(name)
    att = {'table': {'columns': columns, 'version': 1}, 'table_name': table}


    #
    # Transform Data
    #

    ### IF Data
    if len(rows) > 0 :

        # test on memoryview:
        col_num = [ i for i in range(0,len(rows)) if isinstance(rows[0][i],memoryview) ]
        print(col_num)
        exit(0)

        # Remove columns 'DIREPL_PID', 'DIREPL_STATUS' and create JSON
        for r in rows :
            print(type(r[4]))
            if isinstance(r[4],memoryview) :
                print(r[4].tobytes())
        exit(-1)
        df = pd.DataFrame(rows, columns=colum_names).drop(columns=['DIREPL_PID', 'DIREPL_STATUS'])

        varbinary_cols = [c["name"] for c in att['table']['columns'] if c['type']['hana'] == 'VARBINARY' ]
        decode_successful = dict()
        for vb in varbinary_cols :
            decode_successful[vb] = False
            for codec in api.config.codecs:
                try:
                    df[vb] = df[vb].str.decode(codec)
                except :
                    log('Decode failed: \'{}\''.format(codec), 'warning')
                    continue
                log('Decode successful: \'{}\''.format(codec))
                decode_successful[vb]  = True
                break
            if not decode_successful[vb] :
                log('Decode with utf-8 and ignore errors: \'{}\''.format(vb))
                try :
                    df[vb] = df[vb].str.decode('utf-8','ignore')
                    decode_successful[vb] = True
                except :
                    log('Decode failed completely: \'{}\''.format(vb), 'error')

        if len(decode_successful) == 0 or all(v for v in decode_successful.values()) :
            ### DATA to OUTPUT
            if api.config.output == 'JSON':
                data = df.to_json(orient='records', date_format='%Y%m%d %H:%M:%S')
            else :
                data = df.to_csv(index = False,header=False, date_format='%Y%m%d %H:%M:%S')
            api.send("output", api.Message(attributes=att, body=data))
            log("Data send to file. Records: {}, Data: {}".format(df.shape[0], len(msg.body)))

        else :
            ### NODATA To NODATA due to error
            log('Due to failed decoding no transformation and no data send!')
            api.send("nodata", api.Message(attributes=att,body = 'NODATA due to DATA ERROR'))

    ### NODATA To NODATA
    else:
        api.send("nodata", api.Message(attributes=att,body = 'NODATA'))
        log("No Data send!")


api.set_port_callback("input", on_input)
