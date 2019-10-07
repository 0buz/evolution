# import sys
# sys.path.append('/home/adrian/all/evolution/evolution/scripts/')
# import os
# os.getcwd()
# os.chdir("/home/adrian/all/evolution/evolution")

from datetime import date
import re
from selenium.common import exceptions as SE
import time

def filename(fname, ftype):
    """Returns filename built as fname+current date+.ftype  e.g. rawdata20190830.csv"""
    curr_date = filter(lambda x: x != "-", str(date.today()))  # filter out dashes; this is not a str yet
    return f"{fname}{''.join(curr_date)}.{ftype}"


def remove_white_space(file):
    """Remove whitespace combination (\n followed by one or more \t) and replace with empty string."""
    with open(file, 'r+') as f:
        data = f.read()
        data = re.sub(r'\n\t+', '', data)
        f.seek(0)  # place cursor at the beginning
        f.write(data)
        f.truncate()  # remove and extra text left from the pre-edited version


def try_click(elem,str):
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



from selenium.webdriver.support import expected_conditions as EC

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
