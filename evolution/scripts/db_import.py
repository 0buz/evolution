import os
#os.chdir("/home/adrian/all/evolution/evolution/data/preprocessed")

import psycopg2
from csv import reader


preprocessed_file = "/home/adrian/all/evolution/evolution/data/preprocessed/preprocessed20191007_test.csv"


conn = psycopg2.connect("host=localhost dbname=jobmarket user=pgrole password=rpython")
cur = conn.cursor()
cur.execute('SELECT * FROM jobmarket_job')
one = cur.fetchone()  #tuple
all = cur.fetchall()  #list of tuples

print(one)
print(all)

cur.execute("insert into jobmarket_job(title)")
title = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=20, default='')
    location = models.CharField(max_length=100, default='')
    duration = models.CharField(max_length=30, default='')
    start_date = models.CharField(max_length=30, default='')
    rate = models.CharField(max_length=30, default='')
    recruiter = models.CharField(max_length=50, default='')
    posted_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

with open(preprocessed_file) as f:
    csv_reader = reader(f)
    next(csv_reader)  #skip header
    for row in csv_reader:
        cur.execute("insert into jobmarket_job()")




cur.