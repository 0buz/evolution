import psycopg2
import csv
import re
import datacode.datasource as datasource
from datetime import datetime
from dateutil import parser
from datacode import settings
import os


def get_files_to_import():
    """
    Returns list of files that have been preprocessed, but not imported.
    """

    preprocdir = os.path.join(settings.BASE_DIR+settings.IMPORTED_DIR)
    preproc_files = next(os.walk(preprocdir))[2]      #get only filename from walk tuple; returns list
    unprocessed_files =[file for file in preproc_files if not file.startswith("imported")]
    return unprocessed_files


def import_files(unprocessed_files):
    """
    Loops through list of unprocessed files and imports them to database.
    """

    conn = psycopg2.connect(settings.DB_CREDENTIALS)
    cur = conn.cursor()

    preprocdir = os.path.join(settings.BASE_DIR + settings.IMPORTED_DIR)

    for work_file in unprocessed_files:
        with open(str(os.path.join(preprocdir, work_file)), "r") as f:
            print(f"Processing file {work_file}")
            next(f)  # skip header
            reader = csv.reader(f)
            for row in reader:
                posted_date = parser.parse(row[-1])  # process other date formats
                # posted_date = datetime.strptime(row[-1], '%d/%m/%Y %H:%M:%S')
                created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # print((row[:-1]+[a.strftime('%Y-%m-%d %H:%M:%S'),created_date,'2']))
                cur.execute(
                    "INSERT INTO jobmarket_job(title, description, type, location, duration, start_date, rate, recruiter, posted_date,created_date, owner_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                    (row[:-1] + [posted_date, created_date, '2']))
        print(f"Processed file {work_file}")
        old_file = os.path.join(preprocdir, work_file)
        outputname = re.sub('^preprocessed(.*)csv$', 'imported\\1csv', work_file)
        new_file = os.path.join(preprocdir, outputname)
        os.rename(old_file, new_file)
        conn.commit()
    conn.close()


if __name__ == "__main__":
    file_list=get_files_to_import() # list of preprocessed, but not imported files
    import_files(file_list)


