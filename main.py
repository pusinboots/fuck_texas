from selenium import webdriver
import names
import undetected_chromedriver
import pandas as pd

import random
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")


driver = undetected_chromedriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(20)

OPEN = """//*[@id="post-9"]/div/div/div/div[3]/div[1]/div[2]/div/a/span/img"""
NAME_INPUT = """//*[@id="et_pb_contact_name_0"]"""
EMAIL_INPUT = """//*[@id="et_pb_contact_email_0"]"""
LOCATION_INPUT = """//*[@id="et_pb_contact_location_of_show_0"]"""
DETAILS_INPUT = """//*[@id="et_pb_contact_other_info_0"]"""
SUBMIT = """//*[@id="et_pb_contact_form_0"]/div[2]/form/div/button"""
SUBMIT = """//*[@id="et_pb_contact_form_0"]/div[2]/form/div"""
CLOSE = """//*[@id="popup"]/span/a"""

address_df = pd.read_csv("addresses.csv")

while 1:

    name = names.get_full_name()
    email = f"{name.replace(' ', '.')}{int(random.random() * 100000)}@gmail.com"
    address = next(iter(address_df.sample(n=1).FULL_STREET_NAME)) + " Austin Texas"

    driver.get("https://www.defendkidstx.com")
    time.sleep(random.randrange(1,2) + random.random())
    driver.find_element("xpath", OPEN).click()
    time.sleep(random.randrange(1,2) + random.random())
    driver.find_element("xpath", NAME_INPUT).send_keys(name)
    time.sleep(random.randrange(1,2) + random.random())
    driver.find_element("xpath", EMAIL_INPUT).send_keys(email)
    time.sleep(random.randrange(1,2) + random.random())
    driver.find_element("xpath", LOCATION_INPUT).send_keys(address)

    time.sleep(random.randrange(1,5) + random.random())
    driver.find_element("xpath", SUBMIT).submit()
    time.sleep(5)

    driver.find_element("xpath", CLOSE).click()


    time.sleep(120)
