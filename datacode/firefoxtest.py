from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as SE
from selenium.webdriver.firefox.options import Options

profile = webdriver.FirefoxProfile()
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
profile.set_preference("general.useragent.override", user_agent)
profile.set_preference("network.proxy.type", 1)
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference("webdriver.firefox.marionette", False)

options=Options()
options.set_preference('dom.webnotifications.enabled', False)
#System.setProperty("webdriver.firefox.marionette", "false")
profile.update_preferences()
desired = webdriver.DesiredCapabilities.FIREFOX
desired['marionette'] = False
#binary = FirefoxBinary('D:\\Mozilla Firefoxy\\firefox.exe')
driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired, options=options)
driver.get('https://stackoverflow.com')