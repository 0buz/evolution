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

    def remove_white_space(self):
        """Remove whitespace combination (\n followed by one or more \t) and replace with empty string in file."""
        with open(str(self), 'r+') as f:
            data = f.read()
            data = re.sub(r'\n\t+', '', data)
            f.seek(0)  # place cursor at the beginning
            f.write(data)
            f.truncate()  # remove and extra text left from the pre-edited version
            # log confirmation of completion

    def _output(self):
        """  Returns preprocessed file output location + updated filename
            # look for 'raw' at the start of the string (^)
            # look for 'txt' at the end of the string ($)
            # capture middle group for later use ((.*))
            # replace with 'preprocessed' + captured group (\\1) + 'csv'"""

        self.outputname = re.sub('^raw(.*)txt$', 'preprocessed\\1csv', self.basename)
        self.savepath = f"{os.getcwd()}/evolution/data/preprocessed"
        return os.path.join(self.savepath, self.outputname)

    def data_collect(self):
        """Extracts the raw data and saves it to file."""

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
        # driver.find_element_by_id('txtKey').send_keys("jira")

        # Search
        driver.find_element_by_css_selector('.searchbcontain').click()

        try:
            WebDriverWait(driver, 20).until(
                lambda driver: driver.find_element_by_class_name('job-counter').text.strip() != '')
            job_counter = driver.find_element_by_class_name('job-counter').text
            print(job_counter)
        except SE.TimeoutException as err:
            logging.getLogger("error_logger").error(f"Initial job_counter issue. {err}", exc_info=True)

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
                        # try_click(job,"job")
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
                        ActionChains(driver).send_keys_to_element(temp, Keys.ARROW_UP)
                        ActionChains(driver).send_keys_to_element(temp, Keys.ARROW_DOWN)
                        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, jid)))
                        ActionChains(driver).move_to_element(job).click(job).perform()
                        WebDriverWait(driver, 20).until(WaitForAttrValueChange((By.ID, 'jidval'), jid))

                    innerHTML = driver.find_element_by_id('JobDetailPanel').get_property('innerHTML')
                    f.write("Adding job " + str(count) + innerHTML + "Added job")
                    count += 1
                    # ActionChains(driver).send_keys_to_element(job, Keys.ARROW_DOWN)
                    # WebDriverWait(driver, 20).until(lambda driver: jid == loadedID)      # ensure the right job details loaded by checking the job ids
                jids_old = jids_new

        logging.getLogger("info_logger").info(f"{count} jobs extracted.")
        driver.close()
    #
    # def data_validate(self):
    #     with open(str(self)) as f:
    #         data = f.read()
    #
    #     blocks = re.findall("[\s\S]*?Added job", data)
    #
    #     for block in blocks:
    #         >>>> check block contains one of each



    def data_to_csv(self):
        """Extracts the relevant data from the raw file and saves the extracted data in csv format.
        These will be further (pre)processed and/or uploaded to database via the REST API."""

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
            print(len(items))

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

        rows = list(zip(*jobs))

        file = self._output()

        with open(file, "w") as f:
            header = ['title', 'description', 'type', 'location', 'duration', 'start_date', 'rate', 'recruiter',
                      'posted_date']
            csv_writer = writer(f)
            csv_writer.writerow(header)
            for row in rows:
                csv_writer.writerow(row)

        logging.getLogger("info_logger").info(f"{file} created.")


def get_raw_files():
    """Get all raw files in raw directory; filter out the ones that have already been preprocessed."""
    rawdir = os.path.join(os.getcwd() + "/evolution/data/raw")
    preprocdir = os.path.join(os.getcwd() + "/evolution/data/preprocessed")

    preproc_files = [preproc_file for preproc_file in os.listdir(preprocdir)]

    # get all raw files that do not have a corresponding csv: if file starts with "raw" and the date part ([-12:-4]) does not already exist in the preproc file list
    raw_files = filter(
        lambda raw_file: raw_file.startswith("raw") and not re.findall(raw_file[-12:-4], str(preproc_files)),
        os.listdir(rawdir))
    return list(raw_files)


if __name__ == "__main__":
    test = File()
    test.data_collect()
    test.remove_white_space()
    test.data_to_csv()

# ========== optional ====================

# raw_files = get_raw_files()
# for raw_file in raw_files:
#     work_file = File(raw_file)
#     work_file.remove_white_space()
#     work_file.data_to_csv()
#     logging.getLogger("info_logger").info(f"{work_file} preprocessed.")

# =========================================

#
# rawfile = File('raw20191031test.txt')
#
# #rawfile.data_collect()
# rawfile.data_to_csv()

# with open(str(xxx), "a") as f:
#     f.write("\naaaaaa")
# logging.getLogger("info_logger").info("test jobs extracted.")
#
# curr_date = filter(lambda x: x != "-", str(date.today()))
# basename = f"raw{''.join(curr_date)}xxx.txt"
# outputname = re.sub('^raw(.*)txt$', 'preprocessed\\1csv', basename)


#
# y = open(file,"r")
# x=csvrecords(y)
# print(next(x))
# print(next(x))
# print(next(x))
#
# with open(f"{os.getcwd()}/evolution/data/raw/raw20191029.txt", 'r') as f:
#     data=f.read()
#
#
# print(os.getcwd())
# text = "Added job 6\n \"md_rate\" class=\"jd_value\">£60k+</span></div><div id=\"recruitername\"><label id=\"lbl_recruiter\" class=\"jd_label\">Employment Agency</label><span id=\"md_recruiter\" class=</div></div></div></div></div> Added job 1 \"md_rate\" class=\"jd_value\">£60k+</span></div><div id=\"recruitername\"><label id=\"lbl_recruiter\" class=\"jd_label\">Employment Agency</label><span i class=</div></div></div></div></div>"
#
# data_edit=re.sub("\"","",data)
#
# data_new=re.sub("\s","", data_edit)
#
#
# recruit1 = re.findall("Added job.*\s*.*md_recruiter", text)
# recruit = re.findall(".*Added job.*md_recruiter", data_new)
#
# for item in recruit:
#     print(item)