from hdbcli import dbapi
import yaml

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


config_path = '../testdata/di_replication/select_db/config.yaml'
with open(config_path) as yamls :
    params = yaml.safe_load(yamls)


conn = dbapi.connect(address=params['host'],
                     port=params['port'],
                     user=params['user'],
                     password=params['password'],
                     encrypt=params['useTLS'],
                     sslValidateCertificate=params['validateCertificate'])

table = 'REPLICATION.TEST_BADCHARS'

sql = f'SELECT * FROM {table};'
cursor = conn.cursor()
ret = cursor.execute(sql)
rows = cursor.fetchall()
cursor.close()
conn.close()

columns = []
colum_names = []
for col in cursor.description:
    hanadtype = typemap[col[1]]['hana']
    pddtype = typemap[col[1]]['pandas']
    name = col[0]
    columns.append({"class": pddtype, "name": name, "type": {"hana": hanadtype}})
    colum_names.append(name)
att = {'table': {'columns': columns, 'version': 1}, 'table_name': table}

print(rows[0])

print(type(rows[0][1]))
print(type(rows[0][3]))
print(type(rows[0][4]))
print(type(rows[0][5]))

for col in rows[0] :
    print(type(col))

#col_num = [i for i in range(0, len(rows)) if isinstance(rows[0][i], memoryview)]
