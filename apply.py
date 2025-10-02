"""File that handle all the apply process"""

# pylint: disable=C0301

import pickle
import time
import traceback
import yaml

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utility_function import print_pkl_file_content
from global_variable import *

class Scrapper():
    wait_time = 5
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=1')
    options.add_argument("--log-level=3")  # Suppress all logging levels
    # if len(str(print_pkl_info())) > 20:
    #     options.add_argument('headless')

    options.add_argument("--disable-gpu")  # Disable GPU (helpful in headless mode)
    options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(15)

class ApplyBot():
    "ApplyBot clkass"
    def __init__(self):
        with open("configuration.yml", "r",encoding="utf-8") as file:
            self.configuration_file_data = yaml.load(file, Loader=yaml.FullLoader)

        self.scrapping_window = Scrapper()
        self.username = self.configuration_file_data["welcome_to_the_jungle_username"]
        self.password = self.configuration_file_data["welcome_to_the_jungle_password"]
        self.cookies_file_data = print_pkl_file_content()

    def login(self):
        """Login to Welcome to the jungle"""
        try:
            self.scrapping_window.driver.get(login_page)
            time.sleep(5)
            if len(str(self.cookies_file_data)) > 20:
                cookies = pickle.load(open("cookies.pkl","rb"))
                element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{button_to_triger_login_page_datatestid}"]')))
                element.click()
                time.sleep(5)
                for cookie in cookies:
                    self.scrapping_window.driver.add_cookie(cookie)
                return True

            element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{button_to_triger_login_page_datatestid}"]')))
            element.click()
            time.sleep(10)
            element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{login_button_email_datatestid}"]')))
            #time.sleep(1000)
            element.click()
            time.sleep(2)
            element.send_keys(self.username)
            time.sleep(1)

            element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{login_button_password_datatestid}"]')))
            element.click()
            time.sleep(2)
            element.send_keys(self.password)
            time.sleep(1)
            element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{login_button_submit_datatestid}"]')))
            element.click()
            time.sleep(5)
            element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.XPATH, accept_cookies_xpath)))
            element.click()
            time.sleep(5)
            pickle.dump(self.scrapping_window.driver.get_cookies(), open("cookies.pkl", "wb"))
            time.sleep(5)
            return True
        except:
            import traceback
            traceback.print_exc()
            return False
        
def apply_script():
    """Script that will do the apply"""
    auto_apply = ApplyBot()
    if auto_apply.login() is False:
        print("Login Failed goodbye")
        return
    
    print("Good login")
