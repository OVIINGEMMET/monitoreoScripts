import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import binascii
import hashlib
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'
global browser
browser = webdriver.Firefox(capabilities=firefox_capabilities)
browser.get('https://www.google.com')
print(browser.page_source)