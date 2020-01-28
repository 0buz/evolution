import psycopg2
import csv
import re
import datacode.datasource as datasource
from datetime import datetime
import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')
# import sys
# sys.path.append('/home/adrian/all/evolution/')
print(os.getcwd())
# os.chdir("~/all/evolution/evolution")

conn = psycopg2.connect("dbname=jobmarket user=pgrole host=localhost password=rpython")
cur = conn.cursor()
#
# cur.execute("select * from jobmarket_job limit 100;")
# res = cur.fetchall()
#
# for item in res:
#     print(item)


def format_date(date):

    if datetime.strptime(date,)


     return date.strftime('%Y-%m-%d %H:%M:%S')

    posted_date = datetime.strptime(row[-1], '%d/%m/%Y %H:%M:%S')
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    preprocdir = os.path.join(os.getcwd() + "/datacode/data/preprocessed")
    preproc_files = next(os.walk(preprocdir))[2]      #get only filename from walk tuple; returns list
    unprocessed_files =[file for file in preproc_files if not file.startswith("imported")]

    for work_file in unprocessed_files[:2]:
        with open(str(os.path.join(preprocdir,work_file)), "r") as f:
            print(f"Processing file {work_file}")
            next(f)  # skip header
            reader = csv.reader(f)
            for row in reader:
                posted_date = datetime.strptime(row[-1], '%d/%m/%Y %H:%M:%S')
                created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
               # print((row[:-1]+[a.strftime('%Y-%m-%d %H:%M:%S'),created_date,'2']))
                cur.execute("INSERT INTO jobmarket_job(title, description, type, location, duration, start_date, rate, recruiter, posted_date,created_date, owner_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                            (row[:-1]+[posted_date.strftime('%Y-%m-%d %H:%M:%S'),created_date,'2']))
        print(f"Processed file {work_file}")
        old_file=os.path.join(preprocdir,work_file)
        outputname = re.sub('^preprocessed(.*)csv$', 'imported\\1csv', work_file)
        new_file=os.path.join(preprocdir,outputname)
        os.rename(old_file,new_file)

        conn.commit()
    conn.close()


