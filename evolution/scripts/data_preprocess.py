import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')

from bs4 import BeautifulSoup
from lxml import html
from csv import reader, writer, DictReader, DictWriter
import evolution.utils as utils
import re




rawfile = "/home/adrian/all/evolution/evolution/data/raw/raw20191001.txt"
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
    'start_date':'startdate',
    'rate':'rate',
    'recruiter':'md_recruiter',
    'posted_date':'md_posted_date'
}

jobs=[]

for html_id_key, html_id_value in html_ids.items():
    items = soup.find_all(id=f"{html_id_value}")
    # list comprehension on job columns; special handling for Location, Duration, Start Date and Rate to remove div text; preferred Python route over html xpath to do this
    column = [re.sub(html_id_key, '', item.get_text()) if (html_id_key == 'Location') or (html_id_key == 'Duration') or (html_id_key == 'Start Date') or (html_id_key == 'Rate') else item.get_text() for item in items]

    print(html_id_value, len(column), column) # to be logged
    jobs.append(column)   # append the separate lists to the main job list

rows = list(zip(*jobs))

for item in rows:
    print("\n",item)


file = utils.fileoutput('preprocessed','preprocessed','csv')

with open(file, "w") as f:
    csv_writer = writer(f)
    csv_writer.writerow(html_ids)  # write header; by default this is html_ids.keys()
    for row in rows:
        csv_writer.writerow(row)




