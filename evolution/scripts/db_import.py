import os
#os.chdir("/home/adrian/all/evolution/evolution/data/preprocessed")

import psycopg2
from csv import reader


preprocessed_file = "/home/adrian/all/evolution/evolution/data/preprocessed/preprocessed20191007_test.csv"

with open(preprocessed_file) as f:
    csv_reader = reader(f)
    next(csv_reader)  #skip header
    for row in csv_reader:
        print(row)



conn = psycopg2.connect("host=localhost dbname=jobmarket user=pgrole password=rpython")
cur = conn.cursor()
cur.execute('SELECT * FROM jobmarket_job')
one = cur.fetchone()  #tuple
all = cur.fetchall()  #list of tuples

print(one)
print(all)

cur.