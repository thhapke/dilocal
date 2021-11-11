import os

import csv

typemap = {}
with open(os.path.join('misc','hanatypecode.csv')) as csvfile :
    rows = csv.reader(csvfile,delimiter = ',')
    for row in rows :
        typemap[int(row[0])] = {'HANA':row[1],'pandas':row[2]}
print(typemap)
