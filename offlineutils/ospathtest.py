import os

file = "/shared/thorstenh/MultipleTableTest/ADDRESS.csv"
tablename = os.path.basename(file).split('.')[0]
print(tablename)