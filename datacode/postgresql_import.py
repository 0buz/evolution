import psycopg2
import csv
from datetime import datetime
import datacode.datasource as datasource
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


if __name__ == "__main__":
    unprocessed_files=datasource.get_raw_files()
    for file in unprocessed_files[:2]:
        workfile=datasource.File(file)
        with open(workfile, "r") as f:
            next(f)  # skip header
            reader = csv.reader(f)
            for row in reader:
                posted_date = datetime.strptime(row[-1], '%d/%m/%Y %H:%M:%S')
                created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
               # print((row[:-1]+[a.strftime('%Y-%m-%d %H:%M:%S'),created_date,'2']))
                cur.execute("INSERT INTO jobmarket_job(title, description, type, location, duration, start_date, rate, recruiter, posted_date,created_date, owner_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                            (row[:-1]+[posted_date.strftime('%Y-%m-%d %H:%M:%S'),created_date,'2']))
        print(f"Processed file {file}")

        conn.commit()
    conn.close()


