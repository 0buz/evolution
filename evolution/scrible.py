import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')
# import sys
# sys.path.append('/home/adrian/all/evolution/')
os.getcwd()
# os.chdir("~/all/evolution/evolution")
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions as SE
from datetime import date
from bs4 import BeautifulSoup
from csv import writer, DictReader
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count

class File:
    """Class enabling the collection, preprocessing, and upload of data."""

    def __init__(self, *args):
        curr_date = filter(lambda x: x != "-", str(date.today()))  # filter out dashes; this is not a str yet

        if not args:  # optional arg for user-defined filename
            self.basename = f"raw{''.join(curr_date)}.txt"  # generated filename
        else:
            self.basename = args[0]  # filename based on optional arg

        self.savepath = f"{os.getcwd()}/evolution/data/raw"  # path based on working directory
        self.file = os.path.join(self.savepath, self.basename)

    def __repr__(self):
        return f"{self.file}"

    def _output(self):
        """  Returns preprocessed file output location + updated filename
            # look for 'raw' at the start of the string (^)
            # look for 'txt' at the end of the string ($)
            # capture middle group for later use ((.*))
            # replace with 'preprocessed' + captured group (\\1) + 'csv'"""

        self.outputname = re.sub('^raw(.*)txt$', 'preprocessed\\1csv', self.basename)
        self.savepath = f"{os.getcwd()}/evolution/data/preprocessed"
        return os.path.join(self.savepath, self.outputname)

    def data_to_csv(self):
        """Extracts the relevant data from the raw file and saves the extracted data in csv format.
        These will be further (pre)processed and/or uploaded to database via the REST API."""

        start = time.process_time()
        with open(str(self)) as f:
            html = f.read()
        print("Read raw file:", time.process_time() - start)

        start = time.process_time()
        soup = BeautifulSoup(html, 'lxml')

        html_ids = {
            'title': 'td_jobpositionlink',
            'description': 'md_skills',
            'type': 'td_job_type',
            'location': 'location',
            'duration': 'duration',
            'start date': 'startdate',
            'rate': 'rate',
            'recruiter': 'md_recruiter',
            'posted date': 'md_posted_date'
        }
        print("Build soup object:",time.process_time() - start)

        start = time.process_time()
        jobs = []

        for html_id_key, html_id_value in html_ids.items():
            items = soup.find_all(id=f"{html_id_value}")
            #print(len(items))
            # list comprehension on job columns with preprocessing in specific cases
            column = [
                re.sub(html_id_key.title(), "", item.get_text())
                if (html_id_key == 'location') or (html_id_key == 'duration') or (html_id_key == 'start date') or (html_id_key == 'rate')
                else ''.join(re.sub("\\/", "", item.get_text()).split()) if html_id_key == 'type'   # <<< remove any "/" and strip spaces
                else item.get_text()
                for item in items
            ]
            print(html_id_value, len(column))  # to be logged
            jobs.append(column)  # append the separate lists to the main job list

        print("Jobs creation:",time.process_time() - start)

        start = time.process_time()
        rows = list(zip(*jobs))
        print("Zipping:",time.process_time() - start)
        file = self._output()

        with open(file, "w") as f:
            header = ['title', 'description', 'type', 'location', 'duration', 'start_date', 'rate', 'recruiter',
                      'posted_date']
            csv_writer = writer(f)
            csv_writer.writerow(header)
            for row in rows:
                csv_writer.writerow(row)

        logging.getLogger("info_logger").info(f"{file} created.")





start = time.process_time()
validation=File('validate_raw20191209.txt')
validation.data_to_csv()
print("Total: {:.4f}".format(time.process_time() - start))
#
# html_ids = {
#     'title': 'td_jobpositionlink',
#     'description': 'md_skills',
#     'type': 'td_job_type',
#     'location': 'location',
#     'duration': 'duration',
#     'start date': 'startdate',
#     'rate': 'rate',
#     'recruiter': 'md_recruiter',
#     'posted date': 'md_posted_date'
# }
#
# for html_id_key, html_id_value in html_ids.items():
#     column = [22]
#     print(html_id_value, len(column))  # to be logged
# if column.count(column[0])==len(html_ids):
#     print("Yep")
# else:
#     print("Nope")
#
# print(len(html_ids))