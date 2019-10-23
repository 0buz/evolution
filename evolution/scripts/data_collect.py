import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evolution.settings')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions as SE
import time
import evolution.utils as utils
import logging

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
#driver.find_element_by_id('txtKey').send_keys("blockchain")

# Search
driver.find_element_by_css_selector('.searchbcontain').click()

try:
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_class_name('job-counter').text.strip() != '')
    job_counter = driver.find_element_by_class_name('job-counter').text
except SE.TimeoutException as err:
    logging.getLogger("error_logger").error(f"Initial job_counter issue. {err}", exc_info=True)
finally:
    print(job_counter)

rawfile = utils.fileoutput('raw','raw', 'txt')
count = 0
whilecount = 0
jids_old = []

with open(rawfile, "w") as f:
    while job_counter:
        jobs = driver.find_elements_by_class_name('jobItem')
        jids_new = [job.get_property('id') for job in jobs]
        jids_diff = [jid for jid in jids_new if jid not in set(jids_old)]   # jids_new minus jids_old
        job_counter = driver.find_element_by_class_name('job-counter').text  # needs to be here otherwise the last batch will be ommited
        whilecount+=1
        for jid in jids_diff:
            job = driver.find_element_by_id(jid)
            WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.ID, 'EmailAlertPrompt')))
            #driver.execute_script("arguments[0].scrollIntoView(true);", job)

            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, jid)))
                ActionChains(driver).move_to_element(job).click(job).perform()
                #utils.try_click(job,"job")
                time.sleep(0.5)
            except SE.TimeoutException as err:
                logging.getLogger("error_logger").error(f"Timeout on job no. {count} >>> {job.text[:30]} >>> try click action.")
                logging.getLogger("error_logger").error(err)

            try:
                WebDriverWait(driver, 20).until(utils.WaitForAttrValueChange((By.ID, 'jidval'), jid))
                loadedID = driver.find_element_by_id('jidval').get_property('value')

            except SE.TimeoutException as err:
                logging.getLogger("error_logger").error(f"TimeoutException on job no. {count} >>> {job.text[:30]} >>> jid {jid} vs loadedID {loadedID}.")
                logging.getLogger("error_logger").error(err)
                #WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ErrorLoadingJobImg')))
                #driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element_by_id(loadedID))
                temp = driver.find_element_by_id(loadedID)
                ActionChains(driver).move_to_element(temp).click(temp).perform()
                time.sleep(0.5)
                ActionChains(driver).send_keys_to_element(job, Keys.ARROW_DOWN)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, jid)))
                ActionChains(driver).move_to_element(job).click(job).perform()
                WebDriverWait(driver, 20).until(utils.WaitForAttrValueChange((By.ID, 'jidval'), jid))

            innerHTML = driver.find_element_by_id('JobDetailPanel').get_property('innerHTML')
            f.write("Added job " + str(count) + innerHTML)
            count += 1
            #ActionChains(driver).send_keys_to_element(job, Keys.ARROW_DOWN)
            # WebDriverWait(driver, 20).until(lambda driver: jid == loadedID)      # ensure the right job details loaded by checking the job ids
        jids_old = jids_new

logging.getLogger("info_logger").info(f"{count} jobs extracted.")

print("Whilecount is ",whilecount)
print("Job counter: ", job_counter)
print("You made it!")

utils.remove_white_space(rawfile)

#driver.close()
logging.getLogger("info_logger").info("jobs extracted.")
