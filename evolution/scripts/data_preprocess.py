from bs4 import BeautifulSoup
from lxml import html
from csv import reader, writer, DictReader, DictWriter
import evolution.utils as utils
import re

remove_white_space("raw20191003_test.txt")

with open("raw20191003_test.txt", "r") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

html_ids = {
    'Title':'td_jobpositionlink',
    'Description':'md_skills',
    'Type':'td_job_type',
    'Location':'location',
    'Duration':'duration',
    'Start Date':'startdate',
    'Rate':'rate',
    'Recruitment Agency':'md_recruiter',
    'Posted Date':'md_posted_date'
}
# syntax: {_____:_____ for __ in ____}
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^^^ REMEMBER SYNTAX   ^^^^^^^^^^^^^^^^^^^^

jobs=[]

for html_id_key, html_id_value in html_ids.items():
    items = soup.find_all(id=f"{html_id_value}")
    # list comprehension on job columns; special handling for Duration, Start Date and Rate to remove div text; preferred Python route over html xpath to do this
    column = [re.sub(html_id_key, '', item.get_text()) if (html_id_key == 'Duration') or (html_id_key == 'Start Date') or (html_id_key == 'Rate') else item.get_text() for item in items]

    print(html_id_value, len(column), column) # to be logged
    jobs.append(column)   # append the separate lists to the main job list

rows = list(zip(*jobs))

for item in rows:
    print("\n",item)


file = utils.filename('preprocessed','csv')

with open(file, "w") as f:
    csv_writer = writer(f)
    csv_writer.writerow(html_ids)  # write header; by default this is html_ids.keys()
    for row in rows:
        csv_writer.writerow(row)





