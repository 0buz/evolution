from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--enable-popup-blocking')
browser = webdriver.Chrome(options=chrome_options,executable_path='/usr/bin/chromedriver')

wait = WebDriverWait(browser, 30)
url = 'https://www.statnews.com/pharmalot/2020/03/13/gilead-coronavirus-covid19-clinical-trials/'
browser.get(url)
wait.until(lambda e: e.execute_script('return document.readyState') != "loading")
#browser.find_element_by_id('stat-modal-close').click()
wait.until(EC.presence_of_all_elements_located([By.CSS_SELECTOR, "p"]))
#browser.switch_to.frame("mc4wp-form-2")
content2 = browser.find_elements_by_xpath('//p')
forms= browser.find_elements_by_xpath('//form//*//p')
content2=content2 + forms
count=0
with open('content2.txt','w') as fh:
    for etxt2 in content2:
        count+=1
        print(etxt2.text)
        print(etxt2.get_property('innerText'))
        fh.write(etxt2.text)
        #fh.write(etxt2.get_property('innerText'))





import urllib.request
import lxml.html
url = 'https://www.statnews.com/pharmalot/2020/03/13/gilead-coronavirus-covid19-clinical-trials/'
ob=urllib.request.urlopen(url).read()
root=lxml.html.document_fromstring(ob)
content=root.xpath("//p")
with open('content1.txt','w') as fh:
    for etxt in content:
        fh.write(etxt.text_content())