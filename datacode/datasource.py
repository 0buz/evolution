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
import psycopg2
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions as SE
from datetime import date
from bs4 import BeautifulSoup
from csv import writer, reader, DictReader
from datetime import datetime
from dateutil import parser
from datacode import settings


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

    file_records=0

    def __init__(self, *args):
        curr_date = filter(lambda x: x != "-", str(date.today()))  # filter out dashes; this is not a str yet

        if not args:  # optional arg for user-defined filename
            self.basename = f"raw{''.join(curr_date)}.txt"  # generated filename
        else:
            self.basename = args[0]  # filename based on optional arg

        self.savepath = f"{settings.BASE_DIR+settings.RAW_DIR}"  # path based on working directory
        self.file = os.path.join(self.savepath, self.basename)

    def __repr__(self):
        return f"{self.file}"

    def _output(self):
        """  Returns preprocessed file output location + updated filename
            # look for 'raw' at the start of the string (^)
            # look for 'txt' at the end of the string ($)
            # capture middle group for later use ((.*))
            # replace with 'preprocessed' + captured group (\\1) + 'csv'"""
        self.savepath = f"{settings.BASE_DIR + settings.IMPORTED_DIR}"
        basename=self.basename
        self.outputname = re.sub('^raw(.*)txt$', 'preprocessed\\1csv', basename)
        return os.path.join(self.savepath, self.outputname)

    def data_collect(self):
        """Extracts the raw data and saves it to file."""

        url = settings.URL
        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--headless')

        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)

        driver.find_element_by_id(settings.AGE).click()
        select = Select(driver.find_element_by_id(settings.AGE))
        select.select_by_index(7)

        # Location
        driver.find_element_by_id(settings.LOC).clear()

        # Industry
        driver.find_element_by_class_name(settings.IND).click()
        checked = driver.find_element_by_id(settings.IND_ALL).get_property('checked')
        if checked:
            driver.find_element_by_id(settings.IND_ALL).click()

        # ITC
        checked = driver.find_element_by_id(settings.IND_ITC).get_property('checked')
        if not checked:
            driver.find_element_by_id(settings.IND_ITC).click()

        # Keyword
        #driver.find_element_by_id('txtKey').send_keys("jira")

        # Search
        driver.find_element_by_css_selector(settings.SEARCH).click()

        try:
            WebDriverWait(driver, 20).until(
                lambda driver: driver.find_element_by_class_name(settings.JOBCOUNTER).text.strip() != '')
            job_counter = driver.find_element_by_class_name(settings.JOBCOUNTER).text
            print(job_counter)
        except SE.TimeoutException as err:
            logging.getLogger("error_logger").error(f"Initial job_counter issue. {err}", exc_info=True)

        count = 0
        whilecount = 0
        jids_old = []

        with open(str(self), "w") as f:
            while job_counter:
                jobs = driver.find_elements_by_class_name(settings.JOBITEM)
                jids_new = [job.get_property('id') for job in jobs]
                jids_diff = [jid for jid in jids_new if jid not in set(jids_old)]  # jids_new minus jids_old
                job_counter = driver.find_element_by_class_name(
                    settings.JOBCOUNTER).text  # needs to be here otherwise the last batch will be omitted
                whilecount += 1
                for i, jid in enumerate(jids_diff):
                    job = driver.find_element_by_id(jid)
                    WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.ID, settings.EMAIL_ALERT)))
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
                        ActionChains(driver).move_to_element(job).click(job.find_element_by_class_name(settings.JOBTITLE)).perform()
                        WebDriverWait(driver, 20).until(WaitForAttrValueChange((By.ID, settings.JOBID), jid))
                        loadedID = driver.find_element_by_id(settings.JOBID).get_property('value')

                    except (SE.TimeoutException, SE.MoveTargetOutOfBoundsException) as err:
                        logging.getLogger("error_logger").error(
                            f"TimeoutException on job no. {count} >>> {job.text[:30]} >>> jid {jid} vs loadedID {loadedID}.")
                        logging.getLogger("error_logger").error(err)
                        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ErrorLoadingJobImg')))
                        # driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element_by_id(loadedID))

                        #prev_jid = jids_diff[jids_diff.index(jid) - 1]
                        prev_jid=jids_diff[i-1]
                        prev_job = driver.find_element_by_id(prev_jid)

                        ActionChains(driver).move_to_element(prev_job).click(
                            prev_job.find_element_by_class_name(settings.JOBTITLE)).perform()   # <<<do this in a for loop?
                        print(f"Clicked on prev_job {prev_jid}.")
                        time.sleep(0.1)
                        ActionChains(driver).move_to_element(job).click(
                            job.find_element_by_class_name(settings.JOBTITLE)).perform()

                        # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, jid)))
                        # ActionChains(driver).move_to_element(job).click(job).perform()
                        WebDriverWait(driver, 20).until(WaitForAttrValueChange((By.ID, settings.JOBID), jid))

                    innerHTML = driver.find_element_by_id(settings.JOBDETAILS).get_property('innerHTML')
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
        """Validates data integrity by ensuring each data block contains one of each html ids.
        If html id does not exist, append block with html id in valid html structure."""
        html_ids = settings.HTML_IDS

        with open(str(self),"r") as f:
            data = f.read()

        blocks = re.findall("[\s\S]*?Added job", data)

        with open(str(self), "w") as f:
            f.seek(0)
            for block in blocks:
                for html_id_value in html_ids.values():
                    append_string = f"<div><span id=\"{html_id_value}\" class=\"jd_value\"><a><span>Unknown</span></a><a></a></span></div> Added job"

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
        html_ids = settings.HTML_IDS
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
        if not all(len(col) == len(next(it)) for col in it):    #ensure all columns have the same length before zipping
            #raise ValueError(f"Columns don't have the same length in {self.file}")
            print(f"Columns don't have the same length in {self.file}")

        print("Jobs creation:",time.process_time() - start)

        start = time.process_time()
        rows = list(zip(*jobs))
        #DataFile.file_records+=len(rows)
        self.record_count=len(rows)
        print("Zipping:",time.process_time() - start)
        outfile = self._output()
        print(f"There are {self.record_count} records in {outfile}.")

        with open(outfile, "w") as f:
            header = ['title', 'description', 'type', 'location', 'duration', 'start_date', 'rate', 'recruiter',
                      'posted_date']
            csv_writer = writer(f)
            csv_writer.writerow(header)
            for row in rows:
                csv_writer.writerow(row)

        logging.getLogger("info_logger").info(f"{outfile} created.")

        return outfile

    def db_import(self, work_file):
        conn = psycopg2.connect(settings.DB_CREDENTIALS)
        cur = conn.cursor()

        with open(work_file, "r") as f:
            print(f"Processing file {work_file}")
            next(f)  # skip header
            csv_reader = reader(f)  #csv.reader
            for row in csv_reader:
                #try:
                    posted_date = parser.parse(row[-1])  # process other date formats
                    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cur.execute(
                        "INSERT INTO jobmarket_job(title, description, type, location, duration, start_date, rate, recruiter, posted_date,created_date, owner_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                        (row[:-1] + [posted_date, created_date, '2']))

                # except Exception as err:
                #     # if Exception, then rollback upload
                #     success = False
                #     current_latest_id = Job.objects.latest('id').id  # get what is now the latest ID
                #     logging.getLogger("error_logger").error(f"{err}. Occurred at record {serializer}.")
                #     items = Job.objects.filter(id__in=[id for id in range(latest_id + 1,
                #                                                           current_latest_id + 1)])  # get all the successfully uploaded records and delete them
                #     for item in items:
                #         item.delete()
                #         # logging.getLogger("error_logger").error(f"{item} record deleted.")
                #     logging.getLogger("error_logger").error(f"Upload rolled back! {len(items)} records deleted.")
                #     break

        print(f"Processed file {work_file}")
        conn.commit()
        conn.close()

        preprocdir = os.path.join(settings.BASE_DIR + settings.IMPORTED_DIR)
        outputname = re.sub('^preprocessed(.*)csv$', 'imported\\1csv', os.path.basename(work_file))
        new_file = os.path.join(preprocdir, outputname)
        os.rename(work_file, new_file)



def get_files(status):
    """Get all files matching the status; filter out the ones that already have that status.
    Status can be one of the following: raw, preprocessed, imported."""

    if status not in ('raw','preprocessed','imported'):
        raise ValueError(f"get_files function argument must be one of the following: raw, preprocessed, imported.")

    rawdir = os.path.join(settings.BASE_DIR+settings.RAW_DIR)
    procdir = os.path.join(settings.BASE_DIR + settings.IMPORTED_DIR)   #proc dir contains either preporcessed or imported files

    proc_files = next(os.walk(procdir))[2]  #get only filename from walk tuple; returns list

    # get all files that do not have a corresponding csv: if file name starts with {status} and the date part ([-12:-4]) does not already exist in the preproc file list
    match_files = filter(
        lambda match_file: match_file.startswith(status) and not re.findall(match_file[-12:-4], str(proc_files)),
        os.listdir(rawdir))
    return list(match_files)


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


