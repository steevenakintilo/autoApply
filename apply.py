"""File that handle all the apply process"""

# pylint: disable=C0301
# pylint: disable=W0702

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

from utility_function import print_pkl_file_content , convert_list_to_correct_url_typing
from global_variable import *

class Scrapper():
    wait_time:int = 5
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=1')
    options.add_argument("--log-level=3")  # Suppress all logging levels
    # if len(str(print_pkl_info())) > 20:
    #     options.add_argument('headless')
    
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")
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
        self.username:str = self.configuration_file_data["welcome_to_the_jungle_username"]
        self.password:str = self.configuration_file_data["welcome_to_the_jungle_password"]
        self.job_keyword_list:list[str] = self.configuration_file_data["job_keyword_list"]
        self.is_intership:bool = self.configuration_file_data["is_internship"]
        self.cookies_file_data:str = print_pkl_file_content()
        self.current_url:str = ""
        self.list_of_job_url:list[str] = []

    def login(self) -> bool:
        """Login to Welcome to the jungle"""
        try:
            self.scrapping_window.driver.get(login_page_url)
            time.sleep(5)
            if len(str(self.cookies_file_data)) > 10:
                cookies = pickle.load(open("cookies.pkl","rb"))
                button_to_triger_login_page_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{button_to_triger_login_page_datatestid}"]')))
                button_to_triger_login_page_element.click()
                time.sleep(5)
                for cookie in cookies:
                    self.scrapping_window.driver.add_cookie(cookie)
                return True
            
            button_to_triger_login_page_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{button_to_triger_login_page_datatestid}"]')))
            button_to_triger_login_page_element.click()
            time.sleep(10)
            login_button_email_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{login_button_email_datatestid}"]')))
            #time.sleep(1000)
            login_button_email_element.click()
            time.sleep(2)
            login_button_email_element.send_keys(self.username)
            time.sleep(1)

            login_button_password_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{login_button_password_datatestid}"]')))
            login_button_password_element.click()
            time.sleep(2)
            login_button_password_element.send_keys(self.password)
            time.sleep(1)
            login_button_submit_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{login_button_submit_datatestid}"]')))
            login_button_submit_element.click()
            time.sleep(5)
            try:
                accept_cookies_xpath_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.XPATH, accept_cookies_xpath)))
                accept_cookies_xpath_element.click()
                time.sleep(5)
            except:
                pass
            pickle.dump(self.scrapping_window.driver.get_cookies(), open("cookies.pkl", "wb"))
            time.sleep(5)
            return True
        except:
            traceback.print_exc()
            return False

    def search_job_offers(self) -> None:
        """Searching job offer"""
        grid = False
        job_type = permanent_job_url_typing
        if self.is_intership:
            job_type = internship_job_url_typing
        for words in self.job_keyword_list:
            current_job_page = f"{job_page_url}{convert_list_to_correct_url_typing(words)}{job_type}"
            self.scrapping_window.driver.get(current_job_page)
            if grid is False:
                grid_view_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.XPATH, grid_view_xpath)))
                grid_view_element.click()
                grid = True
                time.sleep(5)
            self.current_url = current_job_page
            for page_number in range(5):
                if page_number != 0:
                    time.sleep(5)
                    try:
                        self.scrapping_window.driver.get(f"{current_job_page}&page={str(page_number+1)}")
                        time.sleep(wait_time)
                    except:
                        traceback.print_exc()
                        self.scrapping_window.driver.get(f"{current_job_page}&page={str(page_number+1)}")
                        self.scrapping_window.driver.refresh()
                        time.sleep(15)
                self.get_job_info_by_page()

        print(self.list_of_job_url)
        print(len(self.list_of_job_url))
        time.sleep(1000)

    def get_job_info_by_page(self) -> None:
        """Getting all jobs info of each page"""

        all_jobs_of_the_page_element  = WebDriverWait(self.scrapping_window.driver,wait_time).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'[data-testid="{all_jobs_of_the_page_datatestid}"]')))
        index = 1
        while index < len(all_jobs_of_the_page_element):
            try:
                current_job_url = f"/html/body/div[1]/div/div/div/div[3]/div/div[3]/div/ul/li[{str(index)}]/div/div/div/a"
                current_job_url_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
                EC.presence_of_element_located((By.XPATH, current_job_url)))
                if current_job_url_element.get_property("href") not in self.list_of_job_url:
                    self.list_of_job_url.append(current_job_url_element.get_property("href"))
                time.sleep(0.2)
                self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", current_job_url_element)
                index+=1
            except:
                try:
                    profile_dissmiss_button_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{profile_dissmiss_button_datatestid}"]')))
                    profile_dissmiss_button_element.click()
                    index-=1
                except:
                    traceback.print_exc()

def apply_script():
    """Script that will do the apply"""
    auto_apply = ApplyBot()
    # 1 Login

    if auto_apply.login() is False:
        print("Login Failed goodbye")
        return
    
    # 2 Search job offers

    auto_apply.search_job_offers()
    print(auto_apply.list_of_job_url)
    time.sleep(1000)