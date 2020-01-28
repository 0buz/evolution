import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')
# # import sys
# # sys.path.append('/home/adrian/all/evolution/')
# os.getcwd()
# # os.chdir("~/all/evolution/evolution")
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


class WaitForAttrValueChange:
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


class DataFile:
    """Class enabling the collection, preprocessing, and upload of data."""

    def __init__(self, *args):
        curr_date = filter(lambda x: x != "-", str(date.today()))  # filter out dashes; this is not a str yet

        if not args:  # optional arg for user-defined filename
            self.basename = f"raw{''.join(curr_date)}.txt"  # generated filename
        else:
            self.basename = args[0]  # filename based on optional arg

        self.savepath = f"{os.getcwd()}/datacode/data/raw"  # path based on working directory
        self.file = os.path.join(self.savepath, self.basename)

    def __repr__(self):
        return f"{self.file}"

    def _output(self,action):
        """  Returns preprocessed file output location + updated filename
            # look for 'raw' at the start of the string (^)
            # look for 'txt' at the end of the string ($)
            # capture middle group for later use ((.*))
            # replace with 'preprocessed' + captured group (\\1) + 'csv'"""

        self.outputname = re.sub('^raw(.*)txt$', action+'\\1csv', self.basename)
        self.savepath = f"{os.getcwd()}/datacode/data/preprocessed"
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

                    # try:
                    #     WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, jid)))
                    #     ActionChains(driver).move_to_element(job).click(job.find_element_by_class_name('jobResultsTitle')).perform()
                    #     # try_click(job,"job")
                    #
                    # except SE.MoveTargetOutOfBoundsException as err:
                    #     logging.getLogger("error_logger").error(
                    #         f"Timeout on job no. {count} >>> {job.text[:30]} >>> try click action.")
                    #     logging.getLogger("error_logger").error(err)

                    try:
                        time.sleep(0.2)
                        ActionChains(driver).move_to_element(job).click(job.find_element_by_class_name('jobResultsTitle')).perform()
                        WebDriverWait(driver, 20).until(WaitForAttrValueChange((By.ID, 'jidval'), jid))
                        loadedID = driver.find_element_by_id('jidval').get_property('value')

                    except (SE.TimeoutException, SE.MoveTargetOutOfBoundsException) as err:
                        logging.getLogger("error_logger").error(
                            f"TimeoutException on job no. {count} >>> {job.text[:30]} >>> jid {jid} vs loadedID {loadedID}.")
                        logging.getLogger("error_logger").error(err)
                        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ErrorLoadingJobImg')))
                        # driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element_by_id(loadedID))

                        prev_jid = jids_diff[jids_diff.index(jid) - 1]
                        prev_job = driver.find_element_by_id(prev_jid)

                        ActionChains(driver).move_to_element(prev_job).click(
                            prev_job.find_element_by_class_name('jobResultsTitle')).perform()   # <<<do this in a for loop?
                        print(f"Clicked on prev_job {prev_jid}.")
                        time.sleep(0.1)
                        ActionChains(driver).move_to_element(job).click(
                            job.find_element_by_class_name('jobResultsTitle')).perform()

                        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, jid)))
                        # ActionChains(driver).move_to_element(job).click(job).perform()
                        WebDriverWait(driver, 20).until(WaitForAttrValueChange((By.ID, 'jidval'), jid))

                    innerHTML = driver.find_element_by_id('JobDetailPanel').get_property('innerHTML')
                    f.write("\n\nAdding job " + str(count) + innerHTML + "Added job")
                    count += 1
                    # ActionChains(driver).send_keys_to_element(job, Keys.ARROW_DOWN)
                    # WebDriverWait(driver, 20).until(lambda driver: jid == loadedID)      # ensure the right job details loaded by checking the job ids
                jids_old = jids_new

        logging.getLogger("info_logger").info(f"{count} jobs extracted.")
        driver.close()

    def remove_white_space(self):
        """Remove whitespace combination (\n followed by one or more \t) and replace with empty string in file."""
        with open(str(self), 'r+') as f:
            data = f.read()
            data = re.sub(r'\n\t+', '', data)
            f.seek(0)  # place cursor at the beginning
            f.write(data)
            f.truncate()  # remove and extra text left from the pre-edited version
            # log confirmation of completion

    def data_validate(self):
        """Validates data integrity by ensuring each """
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

        with open(str(self),"r") as f:
            data = f.read()

        blocks = re.findall("[\s\S]*?Added job", data)

        with open(str(self), "w") as f:
            f.seek(0)
            for block in blocks:
                for html_id_value in html_ids.values():
                    append_string = f"<div><span id=\"{html_id_value}\" class=\"jd_value\"><a><span>Unknown</span></a><a></a></span></div> Added job"
                    #append_string = f"<div id=\"recruitername\"><span id=\"{html_id_value}\" class=\"jd_value\"><a ><span>Unknown</span></a></span></div> Added job"
                    #append_string = f"\n<div id=\"recruitername\"><label id=\"lbl_recruiter\" class=\"jd_label\">Recruiter</label><span id=\"{html_id_value}\" class=\"jd_value\"><a href=\"\" target=\"_self\" title=\"View more information about\"><span><span>Unknown</span></span></a><a></a></span></div> Added job"

                    found = re.findall(html_id_value, block)
                    if not found:
                       # print(block)
                        print("block=", len(block))
                        block=re.sub("Added job",append_string,block)
                        #block=block[:-(len(append_string)+41)] + append_string  # overwrite the end of the block with append_string
                        print("block_updated>>>>>>>>>>", block)
                f.write(block)
            # log confirmation of completion

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
            #print(f"Col count in column:{len(jobs[0])}")

        it=iter(jobs)
        if not all(len(col) == len(next(it)) for col in it):    #ensure all columns has the same length before zipping
            #raise ValueError(f"Columns don't have the same length in {self.file}")
            print(f"Columns don't have the same length in {self.file}")

        print("Jobs creation:",time.process_time() - start)

        start = time.process_time()
        rows = list(zip(*jobs))
        print("Zipping:",time.process_time() - start)
        outfile = self._output('preprocessed')

        with open(outfile, "w") as f:
            header = ['title', 'description', 'type', 'location', 'duration', 'start_date', 'rate', 'recruiter',
                      'posted_date']
            csv_writer = writer(f)
            csv_writer.writerow(header)
            for row in rows:
                csv_writer.writerow(row)

        logging.getLogger("info_logger").info(f"{outfile} created.")

        return outfile


def get_raw_files():
    """Get all raw files in raw directory; filter out the ones that have already been preprocessed."""
    rawdir = os.path.join(os.getcwd() + "/datacode/data/raw")
    preprocdir = os.path.join(os.getcwd() + "/datacode/data/preprocessed")

    preproc_files = next(os.walk(preprocdir))[2]  #get only filename from walk tuple; returns list

    print(preproc_files)

    # get all raw files that do not have a corresponding csv: if file name starts with "raw" and the date part ([-12:-4]) does not already exist in the preproc file list
    raw_files = filter(
        lambda raw_file: raw_file.startswith("raw") and not re.findall(raw_file[-12:-4], str(preproc_files)),
        os.listdir(rawdir))
    return list(raw_files)


if __name__ == "__main__":
    test = DataFile()
    test.data_collect()
    test.remove_white_space()
    test.data_validate()
    test.data_to_csv()

    # validation=DataFile('validate_raw20191209.txt')
    # validation.remove_white_space()
    # validation.data_validate()
    # validation.data_to_csv()