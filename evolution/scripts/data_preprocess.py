import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')

from bs4 import BeautifulSoup
from lxml import html
from csv import reader, writer, DictReader, DictWriter
import csv
import evolution.utils as utils
import re




rawfile = "/home/adrian/all/evolution/evolution/data/raw/jiraraw20191014.txt"
utils.remove_white_space(rawfile)

with open(rawfile) as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

html_ids = {
    'title':'td_jobpositionlink',
    'description':'md_skills',
    'type':'td_job_type',
    'location':'location',
    'duration':'duration',
    'start date':'startdate',
    'rate':'rate',
    'recruiter':'md_recruiter',
    'posted date':'md_posted_date'
}

jobs=[]

for html_id_key, html_id_value in html_ids.items():
    items = soup.find_all(id=f"{html_id_value}")
    # list comprehension on job columns; special handling for Location, Duration, Start Date and Rate to remove div text; preferred Python route over html xpath to do this
    column = [re.sub(html_id_key.title(), '', item.get_text()) if (html_id_key == 'location') or (html_id_key == 'duration') or (html_id_key == 'start date') or (html_id_key == 'rate') else item.get_text() for item in items]

    print(html_id_value, len(column), column) # to be logged
    jobs.append(column)   # append the separate lists to the main job list

rows = list(zip(*jobs))

# for item in rows:
#     print("\n",item)


file = utils.fileoutput('preprocessed','preprocessed','csv')

with open(file, "w") as f:
    csv_writer = writer(f, quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerow(html_ids)  # write header; by default this is html_ids.keys()
    for row in rows:
        csv_writer.writerow(row)




