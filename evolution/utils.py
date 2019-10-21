# import sys
# sys.path.append('/home/adrian/all/evolution/evolution/scripts/')
import os
# os.getcwd()
# os.chdir("~/all/evolution/evolution")
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import re
from selenium.common import exceptions as SE
import time
import csv


def fileoutput(flocation, fname, ftype):
    """Returns the fullpath for the file to be saved. e.g. flocation+fname+current date+.ftype  e.g. ../foldername/filename20190830.csv"""
    curr_date = filter(lambda x: x != "-", str(date.today()))  # filter out dashes; this is not a str yet
    basename=f"{fname}{''.join(curr_date)}.{ftype}"    #file name
    savepath = f"{os.getcwd()}/evolution/data/{flocation}"      # path based on working directory
    return os.path.join(savepath, basename)

def preprocessed_fileoutput(flocation, fname, ftype):
    """Returns the fullpath for the file to be saved. e.g. flocation+fname+.ftype  e.g. ../foldername/filename.csv"""
    curr_date = filter(lambda x: x != "-", str(date.today()))  # filter out dashes; this is not a str yet
    basename=f"{fname}{''.join(curr_date)}.{ftype}"    #file name
    savepath = f"{os.getcwd()}/evolution/data/{flocation}"      # path based on working directory
    return os.path.join(savepath, basename)

def remove_white_space(file):
    """Remove whitespace combination (\n followed by one or more \t) and replace with empty string."""
    with open(file, 'r+') as f:
        data = f.read()
        data = re.sub(r'\n\t+', '', data)
        f.seek(0)  # place cursor at the beginning
        f.write(data)
        f.truncate()  # remove and extra text left from the pre-edited version
        #log confirmation of completion


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


# def csvrecords(file):
#     with open(file,"r") as f:
#         datareader = csv.DictReader(f)
#         for item in datareader:
#             yield item


def csvrecords(file):
    for item in csv.DictReader(file):
        yield item

#
#file = "/home/adrian/all/evolution/evolution/data/preprocessed/preprocessed20191007updated.csv"
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