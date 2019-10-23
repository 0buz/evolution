import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')
# import sys
# sys.path.append('/home/adrian/all/evolution/evolution/scripts/')
os.getcwd()
# os.chdir("~/all/evolution/evolution")
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions as SE
import time
from datetime import date
from selenium.common import exceptions as SE
from bs4 import BeautifulSoup
from csv import reader, writer, DictReader, DictWriter
import re
import logging



class WaitForAttrValueChange(object):
    def __init__(self, locator, val_):
        self.locator = locator
        self.val = val_

    def __call__(self, driver):
        try:
            attr_value = EC._find_element(driver, self.locator).get_property('value')
            return attr_value.startswith(self.val)
        except SE.StaleElementReferenceException:
            return False


class File:
    def __init__(self):
        curr_date = filter(lambda x: x != "-", str(date.today()))  # filter out dashes; this is not a str yet
        self.basename = f"raw{''.join(curr_date)}.txt"  # file name
        self.savepath = f"{os.getcwd()}/evolution/data/raw"  # path based on working directory
        self.file = os.path.join(self.savepath, self.basename)

    def __repr__(self):
        return f"{self.file}"

    def output(self):
        """ # look for 'raw' at the start of the string (^)
            # look for 'txt' at the end of the string ($)
            # capture middle group for later use ((.*))
            # replace with 'preprocessed' + captured group (\\1) + 'csv'"""
        self.outputname = re.sub('^raw(.*)txt$', 'preprocessed\\1csv', self.basename)
        self.savepath = f"{os.getcwd()}/evolution/data/preprocessed"
        return os.path.join(self.savepath, self.outputname)

    def _remove_white_space(self):
        """Remove whitespace combination (\n followed by one or more \t) and replace with empty string."""
        with open(str(self), 'r+') as f:
            data = f.read()
            data = re.sub(r'\n\t+', '', data)
            f.seek(0)  # place cursor at the beginning
            f.write(data)
            f.truncate()  # remove and extra text left from the pre-edited version
            # log confirmation of completion

    def data_collect(self):
        url = 'https://www.jobserve.com'

        driver = webdriver.Chrome()
        driver.get(url)

        driver.find_element_by_id('selAge').click()
        select = Select(driver.find_element_by_id('selAge'))
        select.select_by_index(7)

        # Location
        driver.find_element_by_id('txtLoc').clear()

        # Industry
        driver.find_element_by_class_name('ui-dropdownchecklist-text').click()
        checked = driver.find_element_by_id('ddcl-selInd-i0').get_property('checked')
        if checked:
            driver.find_element_by_id('ddcl-selInd-i0').click()

        # ITC
        checked = driver.find_element_by_id('ddcl-selInd-i14').get_property('checked')
        if not checked:
            driver.find_element_by_id('ddcl-selInd-i14').click()

        # Keyword
        driver.find_element_by_id('txtKey').send_keys("jira")

        # Search
        driver.find_element_by_css_selector('.searchbcontain').click()

        try:
            WebDriverWait(driver, 10).until(
                lambda driver: driver.find_element_by_class_name('job-counter').text.strip() != '')
            job_counter = driver.find_element_by_class_name('job-counter').text
        except SE.TimeoutException as err:
            logging.getLogger("error_logger").error(f"Initial job_counter issue. {err}", exc_info=True)
        finally:
            print(job_counter)

        count = 0
        whilecount = 0
        jids_old = []

        with open(str(self), "w") as f:
            while job_counter:
                jobs = driver.find_elements_by_class_name('jobItem')
                jids_new = [job.get_property('id') for job in jobs]
                jids_diff = [jid for jid in jids_new if jid not in set(jids_old)]  # jids_new minus jids_old
                job_counter = driver.find_element_by_class_name(
                    'job-counter').text  # needs to be here otherwise the last batch will be ommited
                whilecount += 1
                for jid in jids_diff:
                    job = driver.find_element_by_id(jid)
                    WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.ID, 'EmailAlertPrompt')))
                    # driver.execute_script("arguments[0].scrollIntoView(true);", job)

                    try:
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, jid)))
                        ActionChains(driver).move_to_element(job).click(job).perform()
                        # utils.try_click(job,"job")
                        time.sleep(0.2)
                    except SE.TimeoutException as err:
                        logging.getLogger("error_logger").error(
                            f"Timeout on job no. {count} >>> {job.text[:30]} >>> try click action.")
                        logging.getLogger("error_logger").error(err)

                    try:
                        WebDriverWait(driver, 20).until(WaitForAttrValueChange((By.ID, 'jidval'), jid))
                        loadedID = driver.find_element_by_id('jidval').get_property('value')

                    except SE.TimeoutException as err:
                        logging.getLogger("error_logger").error(
                            f"TimeoutException on job no. {count} >>> {job.text[:30]} >>> jid {jid} vs loadedID {loadedID}.")
                        logging.getLogger("error_logger").error(err)
                        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ErrorLoadingJobImg')))
                        # driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element_by_id(loadedID))
                        temp = driver.find_element_by_id(loadedID)
                        ActionChains(driver).move_to_element(temp).click(temp).perform()
                        time.sleep(0.5)
                        ActionChains(driver).send_keys_to_element(job, Keys.ARROW_DOWN)
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, jid)))
                        ActionChains(driver).move_to_element(job).click(job).perform()
                        WebDriverWait(driver, 20).until(WaitForAttrValueChange((By.ID, 'jidval'), jid))

                    innerHTML = driver.find_element_by_id('JobDetailPanel').get_property('innerHTML')
                    f.write("Added job " + str(count) + innerHTML)
                    count += 1
                    # ActionChains(driver).send_keys_to_element(job, Keys.ARROW_DOWN)
                    # WebDriverWait(driver, 20).until(lambda driver: jid == loadedID)      # ensure the right job details loaded by checking the job ids
                jids_old = jids_new

        self._remove_white_space()

        logging.getLogger("info_logger").info(f"{count} jobs extracted.")

    def data_preprocess(self):

        with open(str(self)) as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

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

        jobs = []

        for html_id_key, html_id_value in html_ids.items():
            items = soup.find_all(id=f"{html_id_value}")
            # list comprehension on job columns; special handling for Location, Duration, Start Date and Rate to remove div text; preferred Python route over html xpath to do this
            column = [re.sub(html_id_key.title(), '', item.get_text()) if (html_id_key == 'location') or (
                    html_id_key == 'duration') or (html_id_key == 'start date') or (
                                                                                  html_id_key == 'rate') else item.get_text()
                      for item in items]

            print(html_id_value, len(column), column)  # to be logged
            jobs.append(column)  # append the separate lists to the main job list

        rows = list(zip(*jobs))

        # for item in rows:
        #     print("\n",item)

        file = self.output()

        with open(file, "w") as f:
            header = ['title', 'description', 'type', 'location', 'duration', 'start_date', 'rate', 'recruiter',
                      'posted_date']
            csv_writer = writer(f)
            csv_writer.writerow(header)
            for row in rows:
                csv_writer.writerow(row)

        logging.getLogger("info_logger").info(f"{file} created.")


test = File()
with open(str(test), "a") as f:
    f.write("\naaaaaa")

test.output()
with open(str(test.output()), "a") as f:
    f.write("\naaaaaa")

rawfile = File()
rawfile.data_collect()

logging.getLogger("info_logger").info("test jobs extracted.")


def fileoutput(flocation, fname, ftype):
    """Returns the fullpath for the file to be saved. e.g. flocation+fname+current date+.ftype  e.g. ../foldername/filename20190830.csv"""
    curr_date = filter(lambda x: x != "-", str(date.today()))  # filter out dashes; this is not a str yet
    basename = f"{fname}{''.join(curr_date)}.{ftype}"  # file name
    savepath = f"{os.getcwd()}/evolution/data/{flocation}"  # path based on working directory
    return os.path.join(savepath, basename)


base = fileoutput("raw", "dummy", "txt")


def preprocessed_fileoutput(flocation, fname, ftype):
    """Returns the fullpath for the file to be saved. e.g. flocation+fname+.ftype  e.g. ../foldername/filename.csv"""
    curr_date = filter(lambda x: x != "-", str(date.today()))  # filter out dashes; this is not a str yet
    basename = f"{fname}{''.join(curr_date)}.{ftype}"  # file name
    savepath = f"{os.getcwd()}/evolution/data/{flocation}"  # path based on working directory
    return os.path.join(savepath, basename)


def try_click(elem, str):
    result = False
    attempts = 0
    while attempts < 3:
        time.sleep(0.1)
        try:
            elem.click()
            result = True
            break
        except SE.StaleElementReferenceException as err:
            print(f"For element {elem} {str}:", err)
        attempts += 1
    return result


def csvrecords(file):
    """Function to yield one row at a time. This will be used to when uploading csv data via REST API."""
    for item in DictReader(file):
        yield item

#
# file = "/home/adrian/all/evolution/evolution/data/preprocessed/preprocessed20191007updated.csv"
# y = open(file,"r")
# x=csvrecords(y)
# print(next(x))
# print(next(x))
# print(next(x))
# print(next(x))
# print(next(x)["title"])
#
# count = 0
# for row in csvrecords(file):
#     print("Row no", count, row)
#     count+=1

# print("Rows read:",count)
