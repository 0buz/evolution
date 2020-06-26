from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as SE
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
import json
from selenium.webdriver.chrome.options import Options
import pandas as pd


options=webdriver.ChromeOptions()
#options.add_argument('--headless')
#options.add_argument('window-size=1920x1080')
options.add_argument('disable-infobars')
#options.add_argument("--disable-extensions")
#options.add_argument("--disable-notifications")
options.add_argument('start-maximized')
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)
#options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#options.add_argument('--user-agent="Mozilla/76.0.1 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"')

############# Set chrome proxy ###########
# Chrome_Proxy = 'http://135.28.13.11:8888'
# #Chrome_Proxy = 'http://autoproxy.sbc.com/autoproxy.cgi'
# options.add_argument('--proxy-server=%s' % Chrome_Proxy)

driver = webdriver.Chrome(options=options)
#url="https://www.google.com"


url = 'http://www.rera.mp.gov.in/view_project_details.php?id=aDRYYk82L2hhV0R0WHFDSnJRK3FYZz09'
driver.get(url)

#find parent element
proj_info=driver.find_element_by_xpath("//div[@class='col-md-12 box']")

#find all rows in parent element
proj_info_rows = proj_info.find_elements_by_class_name('row')

for row in proj_info_rows:
    try:
        if row.find_element_by_class_name('col-md-8').text.strip() == "":
            print(f"{row.find_element_by_class_name('col-md-4').text} contains only whitespace {row.find_element_by_class_name('col-md-8').text}")
            print('NaN')
        else:
            print(row.find_element_by_class_name('col-md-8').text)
    except SE.NoSuchElementException:
        print('NaN')


eee="""
             g             """

fff=eee.isspace()

select = Select(WebDriverWait(driver, 35).until(EC.visibility_of_element_located((By.ID,'BodyContent__company'))))

for index in range(len(select.options)):
    select.select_by_index(index)
    select = Select(WebDriverWait(driver, 35).until(EC.visibility_of_element_located((By.ID,'BodyContent__company'))))
    print(f"Clicked {select.options[index].text}")

for opt in select:
    # for example
    print(opt.text)
    opt.click()

select_box =driver.find_element_by_xpath("//*[@id='BodyContent__company']")
options = [x.text for x in select_box.find_elements_by_tag_name("option")]
for element in options:
    element.click()


element_timeout = 10
try:
    element_login = EC.presence_of_element_located((By.ID, 'login-button'))
    WebDriverWait(driver, element_timeout).until(element_login)

except SE.TimeoutException:
    print('RC=101,"Error: Failed to load Cisco Website Title"')
    driver.close()
    quit()

print()
print(driver.title)
print()

element_username = EC.presence_of_element_located((By.ID, 'userInput'))
WebDriverWait(driver, element_timeout).until(element_username).send_keys('cisco_userid')

driver.find_element_by_id('login-button').click()

element_password = EC.presence_of_element_located((By.ID, 'password'))
WebDriverWait(driver, element_timeout).until(element_password).send_keys('cisco_userpwd')
print("Entered password!")

######### Login to cisco cloud account ###########


######################## Username ##################
try:
    element_username = EC.presence_of_element_located((By.ID, 'userInput'))
    WebDriverWait(driver, element_timeout).until(element_username).send_keys('cisco_userid')

except SE.TimeoutException:

    print('RC=101,"Error: Failed to login to Cisco Website User"')
    driver.close()
    quit()


# #driver.find_element_by_id('userInput').send_keys(f'{cisco_userid}')
# print('>>>> Username input')
# driver.find_element_by_id('login-button').click()
#
#
# driver.get_screenshot_as_file('/tmp/password.png')
#
# element_password = EC.presence_of_element_located((By.ID, 'password'))
# WebDriverWait(driver, element_timeout).until(element_password).send_keys('cisco_userpwd')
driver.find_element_by_id('login-button').click()
###################### Password ##################
try:
    element_password = EC.presence_of_element_located((By.ID, 'password'))
    WebDriverWait(driver, element_timeout).until(element_password).send_keys('cisco_userpwd')
    print("OK!")

except SE.TimeoutException:
    print('RC=101,"Error: Failed to login to Cisco Website Password"')


time.sleep(5)
#driver.find_element_by_id('password').send_keys(f'{cisco_password}')
print('>>>> Password input')
driver.find_element_by_id('kc-login').click()

elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="map"]/div[1]/div[2]/div[2]/svg')))
table = driver.find_element_by_class_name('leaflet-zoom-animated')

#move perform -> to table
driver.execute_script("arguments[0].scrollIntoView(true);", table)

data = []
for circle in elements:
    #move perform -> to each circle
    ActionChains(driver).move_to_element(circle).perform()
    # wait change mouseover effect
    mouseover = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="neighbourhoodBoundaries"]')))
    data.append(mouseover.text)

print(data[0])





from selenium.webdriver.support.ui import WebDriverWait as wait
next_button=wait(driver, 10).until(EC.presence_of_element_located((By.ID,'searchResults_btn_next')))

# capture the start value from "Showing x-xx of 22 results"
#need this to check against later
ref_val=wait(driver, 10).until(EC.presence_of_element_located((By.ID,'searchResults_start'))).text

while next_button.get_attribute('class') == 'pagebtn':
    # ====== Do whatever relevant here =============================
    page_num = wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.market_paging_pagelink.active'))).text
    print(f"Prices from page {page_num}")
    prices = wait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, ".//span[@class='market_listing_price market_listing_price_with_fee']")))
    for price in prices:
        print(price.text)
    # ================================================================
    next_button.click()
    #wait until ref_val has changed
    wait(driver, 10).until(lambda driver: wait(driver, 10).until(EC.presence_of_element_located((By.ID,'searchResults_start'))).text != ref_val)
    #get the new reference value
    ref_val = wait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchResults_start'))).text








button=driver.find_element_by_xpath(".//div[@class='view_body']/div[2]/span")
print(button.text)


button=driver.find_element_by_xpath("//div[@class='gb_h gb_i']")
print(driver.find_element_by_xpath("//div[@class='gb_h gb_i']").text.strip('G').replace('m','B'))

xx=button.text

if WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "//input[@class='gLFyf gsfi']")))==True:
    print("Now its loaded")
else:
    print("Nope not loaded")


try:
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, "//input[@class='gLFyf gsfi']")))
    print("Now its loaded")
except SE.TimeoutException as err:
    print("Nope not loaded")
    print(err)



inputElement = driver.find_element_by_xpath("//div[@data-rel='phone']")

inputElement.click()

driver.find_element_by_class_name()
btn=WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//form[@name="ebsearch"]/div/span/a[text(),"Select Categories"]')))

ActionChains(driver).move_to_element(btn).click(btn).perform()

WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="toggleAll"]'))).click()

driver.find_element_by_xpath('//button[text()="Save Changes"]').click()


tds = driver.find_elements_by_xpath("//table[@id='sortable-1']/tbody/tr/td[@data-opening-odd]")
tds = driver.find_elements_by_css_selctor("table#sortable-1 > tbody > tr > td[data-opening-odd]")

for td in tds:
    print(td.get_attribute("data-opening-odd"))


driver.execute_script("window.open('');")


iframe=WebDriverWait(driver, 10).until(EC.attr((By.CLASS_NAME, "demo-frame")))
driver.switch_to.frame(iframe)
source=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "draggable")))
destination=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "droppable")))
#destination=driver.find_element_by_id('droppable')

ActionChains(driver).drag_and_drop(source, destination).perform()


WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yfin-usr-qry"]'))).send_keys('apple')


WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div//*[contains(text(),'Symbols')]")))
web_elem_list = driver.find_elements_by_xpath(".//div[@data-test='search-assist-input-sugglst']/div/ul[1]/li/div")
results = pd.DataFrame()


WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@name='bedrooms' and @value='2']/following::label"))).click()



from selenium import webdriver
import time
import selenium

downloadDir='/home/adrian/Downloads'
fp = webdriver.FirefoxProfile()

#profile.set_preference('driver.helperApps.neverAsk.saveToDisk', '"application/pdf":{"action":0,"extensions":["pdf"]')
# profile.set_preference('driver.helperApps.neverAsk.saveToDisk', 'application/pdf')
# profile.set_preference("driver.helperApps.neverAsk.openFile", 'application/pdf')
# profile.set_preference("driver.downLoad.folderList", 0)
# profile.set_preference("driver.download.manager.showWhenStarting", False)
fp.set_preference("driver.download.folderList", 2)
fp.set_preference("driver.download.manager.showWhenStarting", False)
fp.set_preference("driver.download.dir", downloadDir)
fp.set_preference("driver.helperApps.neverAsk.saveToDisk", "attachment/csv")

driver = webdriver.Firefox(firefox_profile=fp)
driver.get("https://amtsblatt.ag.ch/publikationen/")

elem = driver.find_element_by_id("pdf-select-all")
elem.click()
time.sleep(3)

elem2 = driver.find_element_by_class_name("pdf-list-head")
elem2.click()
time.sleep(2)

elem3 = driver.find_element_by_link_text("Exportieren")
elem3.click()

my_iframe=driver.find_element_by_xpath("//iframe[@class='credit-card-iframe-cvv mt1 u-full-width']")
driver.switch_to.frame(my_iframe)

my_iframe=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@class='credit-card-iframe-cvv mt1 u-full-width']")))
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(my_iframe))
driver.switch_to.default_content()
driver.switch_to.default_content()

import sys; print("%s.%s.%s" % sys.version_info[:3])

product_links=driver.find_elements_by_xpath("//div[@class='table-container']//a[contains(@href,'products')]")
product_links=driver.find_elements_by_css_selector("div.table-container a[href*=products]")
