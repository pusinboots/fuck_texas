from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import names
import undetected_chromedriver
import pandas as pd
import openai
import randomname
import ratelimit

import random
import time
from keys import OPEN_AI_KEY
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

openai.api_key = OPEN_AI_KEY

EMAIL_PROVIDERS = ["gmail.com", "yahoo.com", "hotmail.com", "verizon.com", "msn.com"]

OPEN = """//*[@id="post-9"]/div/div/div/div[3]/div[1]/div[2]/div/a/span/img"""
NAME_INPUT = """//*[@id="et_pb_contact_name_0"]"""
EMAIL_INPUT = """//*[@id="et_pb_contact_email_0"]"""
LOCATION_INPUT = """//*[@id="et_pb_contact_location_of_show_0"]"""
DETAILS_INPUT = """//*[@id="et_pb_contact_other_info_0"]"""
SUBMIT = """//*[@id="et_pb_contact_form_0"]/div[2]/form/div/button"""
SUBMIT = """//*[@id="et_pb_contact_form_0"]/div[2]/form/div"""
CLOSE = """//*[@id="popup"]/span/a"""

OPEN_AI_PROMPT = "write a tweet from the perspective of someone who thinks childrens drag shows shouldn't happen without using hashtags"
ADDRESS_CSV_PATH = "addresses.csv"

@ratelimit.limits(calls=15, period=900)
def _generate_text():
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=OPEN_AI_PROMPT,
        temperature=0.8,
        max_tokens=200
    )
    return response.choices[0].text.split('\n\n')[-1]


def generate_text():
    try:
        return _generate_text()
    except ratelimit.RateLimitException:
        return ""


def generate_email():
    # email = f"{name.replace(' ', '.')}{int(random.random() * 100000)}@gmail.com"
    provider = next(iter(random.sample(EMAIL_PROVIDERS, 1)))
    username = randomname.generate().replace("-", "-")
    return f"{username}{random.randrange(0, 1000)}@{provider}"


def generate_address():
    return next(iter(address_df.sample(n=1).FULL_STREET_NAME)) + " Austin Texas"


def human_type(driver, element_path, text):
    element = driver.find_element("xpath", element_path)

    for char in text:
        time.sleep(random.uniform(0, 0.2))
        element.send_keys(char)

    time.sleep(random.uniform(2, 4))

count_sucess = 0
count_fail = 0
if __name__ == "__main__":

    logger.info("STARTING")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = undetected_chromedriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(20)

    address_df = pd.read_csv(ADDRESS_CSV_PATH)
    
    while 1:

        try:
            driver.get("https://www.defendkidstx.com")
            time.sleep(random.uniform(0, 2))

            driver.find_element("xpath", OPEN).click()
            time.sleep(random.uniform(0, 2))

            name = names.get_full_name()
            email = generate_email()
            text = generate_text()
            address = generate_address()

            logger.info(f"Using the following generated info {name=}, {email=}, {address=}, {text=}")

            human_type(driver, NAME_INPUT, name)
            human_type(driver, EMAIL_INPUT, email)
            human_type(driver, LOCATION_INPUT, address)
            human_type(driver, DETAILS_INPUT, text)

            time.sleep(5)
            driver.find_element("xpath", SUBMIT).submit()
            time.sleep(5)

            driver.find_element("xpath", CLOSE).click()
            logger.info("SUCCESSFUL")
            count_sucess += 1

            # 
            time.sleep(15)
        # except NoSuchElementException:
        except Exception as e:
            logger.error(e)
            logger.warning("Hit rate limit, will retry after sleeping")
            count_fail += 1
            time.sleep(30)
        
        
        logger.info(f"{count_sucess=}, {count_fail=}")
