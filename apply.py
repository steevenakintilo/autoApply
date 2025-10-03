"""File that handle all the apply process"""

# pylint: disable=C0301
# pylint: disable=W0702

import pickle
import time
import traceback
import yaml

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utility_function import *
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
        self.list_of_job_inside_welcome_to_the_jungle_url:list[str] = []
        self.list_of_job_outside_welcome_to_the_jungle_url:list[str] = []
        self.sort_job_by_date:bool = self.configuration_file_data["sort_by_date"]
        self.job_already_find:list[str] = print_file_content("all_job_url.txt").lower().split("\n")
        self.number_of_page_to_search:int = self.configuration_file_data["number_of_page_to_search"]
        self.maximum_number_of_offer:int = self.configuration_file_data["maximum_number_of_offer"]
        self.question_mode:bool = False
        self.list_of_questions:list[str] = []
        self.list_of_questions_find:list[str] = print_file_content("list_of_questions.txt").lower().split("\n")
        self.current_post:str = self.configuration_file_data["current_post"]
        self.where_is_the_job:str = self.configuration_file_data["where_is_the_job"]

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
            except NoSuchElementException:
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
        sort_by = sort_by_relevance
        if self.sort_job_by_date:
            sort_by = sort_by_date
        job_type = permanent_job_url_typing
        if self.is_intership:
            job_type = internship_job_url_typing
        for words in self.job_keyword_list:
            current_job_page = f"{job_page_url}{convert_list_to_correct_url_typing(words)}{job_type}{localisation_of_the_job}{self.where_is_the_job}"
            if len(self.list_of_job_url) >= self.maximum_number_of_offer:
                break
            try:
                self.scrapping_window.driver.get(current_job_page)
                time.sleep(2)
            except:
                self.scrapping_window.driver.get(current_job_page)
                self.scrapping_window.driver.refresh()
                time.sleep(15)
            if grid is False:
                grid_view_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.XPATH, grid_view_xpath)))
                grid_view_element.click()
                grid = True
                time.sleep(5)
            self.current_url = current_job_page
            for page_number in range(self.number_of_page_to_search):
                if len(self.list_of_job_url) >= self.maximum_number_of_offer:
                    break
                if page_number != 0:
                    time.sleep(5)
                    try:
                        self.scrapping_window.driver.get(f"{current_job_page}{sort_by}&page={str(page_number+1)}{localisation_of_the_job}{self.where_is_the_job}")
                        time.sleep(wait_time)
                    except:
                        self.scrapping_window.driver.get(f"{current_job_page}{sort_by}&page={str(page_number+1)}{localisation_of_the_job}{self.where_is_the_job}")
                        self.scrapping_window.driver.refresh()
                        time.sleep(15)
                self.get_job_info_by_page()


    def get_job_info_by_page(self) -> None:
        """Getting all jobs info of each page"""
        try:
            all_jobs_of_the_page_element  = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'[data-testid="{all_jobs_of_the_page_datatestid}"]')))
        except:
            time.sleep(5)
            return
        index = 1
        while index < len(all_jobs_of_the_page_element):
            try:
                if len(self.list_of_job_url) >= self.maximum_number_of_offer:
                    return
                current_job_url = f"/html/body/div[1]/div/div/div/div[3]/div/div[3]/div/ul/li[{str(index)}]/div/div/div/a"
                current_job_url_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
                EC.presence_of_element_located((By.XPATH, current_job_url)))
                if current_job_url_element.get_property("href") not in self.list_of_job_url and current_job_url_element.get_property("href").lower() not in self.job_already_find:
                    self.list_of_job_url.append(current_job_url_element.get_property("href"))
                    #write_into_file("all_job_url.txt", current_job_url_element.get_property("href") + "\n")
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

    def parse_job_offer(self,job_offer_url,):
        """Parsing job offer"""
        try:
            self.list_of_questions_find:list[str] = print_file_content("list_of_questions.txt").lower().split("\n")
            time.sleep(2)
            try:
                self.scrapping_window.driver.get(job_offer_url)
                time.sleep(1)
            except:
                self.scrapping_window.driver.get(job_offer_url)
                self.scrapping_window.driver.refresh()
                time.sleep(15)
            
            apply_button_data_testid_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{apply_button_data_testid}"]')))
            
            if apply_button_data_testid_element.get_property("href") is not None:
                self.list_of_job_outside_welcome_to_the_jungle_url.append(job_offer_url)
                return
            
            self.list_of_job_inside_welcome_to_the_jungle_url.append(job_offer_url)
            apply_button_data_testid_element.click()
            time.sleep(5)
           
            #print(apply_form_text_split)
            # Searching for job name:

            try:
                view_more_text_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{view_more_text_datatestid}"]')))
                self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", view_more_text_element)
                time.sleep(1)
                self.scrapping_window.driver.execute_script("arguments[0].click();", view_more_text_element)
                #view_more_text_element.click()
            except:
                pass

            job_offer_text_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
            EC.presence_of_element_located((By.XPATH, job_offer_text_xpath)))
            
            print(job_offer_text_element.text)
            # apply_form_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
            # EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{apply_form_datatestid}"]')))
            # print(apply_form_element.text)

            try:
                current_post_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{current_post_datatestid}"]')))
                if len(current_post_element.text) < 3:
                    current_post_element.click()
                    time.sleep(1)
                    self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", current_post_element)
                    time.sleep(0.5)
                    current_post_element.clear()
                    time.sleep(0.5)
                    current_post_element.send_keys(self.current_post)
                    time.sleep(1)
            except NoSuchElementException:
                pass

            # Searching for question
            try:
                job_xpath2 =  False
                try:
                    job_offer_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
                    EC.presence_of_element_located((By.XPATH, job_offer_question_xpath)))
                except NoSuchElementException:
                    job_offer_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
                    EC.presence_of_element_located((By.XPATH, job_offer_question_xpath2)))
                    job_xpath2 = True
                list_of_question = job_offer_question_element.text.split("\n")[1:]
                if self.question_mode:
                    for text in list_of_question:
                        if len(text) > 5:
                            if text.lower() not in self.list_of_questions and text.lower() not in self.list_of_questions_find:
                                print(text,job_offer_url)
                                #write_into_file("list_of_questions.txt",text.lower()+"#####"+"\n")
                                self.list_of_questions.append(text.lower())
                    
                    #print(apply_form_datatestid_element.text)
                    #print(job_offer_url)
                    #print(".........")
                else:
                    for index , text in enumerate(list_of_question):
                        current_question_xpath = f"/html/body/div[17]/div[2]/div/section/form/fieldset[3]/div[{str(index + 1)}]/div/textarea"
                        if job_xpath2:
                            current_question_xpath = f"/html/body/div[22]/div[2]/div/section/form/fieldset[3]/div[{str(index + 1)}]/div/textarea"
                        current_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                        EC.presence_of_element_located((By.XPATH, current_question_xpath)))
                        current_question_element.click()
                        time.sleep(1)
                        self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", current_question_element)
                        time.sleep(2)
                        if len(text) > 5:
                            if text.lower() not in str(self.list_of_questions_find):
                                write_into_file("list_of_questions.txt",text.lower()+"#####"+"\n")
                                self.list_of_questions.append(text.lower())
                                send_message_discord(f"Answer and add this question to all_questions.txt file with the answer\n {text}", discord_question)
                                return
                            answer = get_answer_from_question_list(text)
                            current_question_element.clear()
                            time.sleep(0.5)
                            current_question_element.send_keys(answer)
                     
                        
            except:
                pass
                
            # Accept consent
            try:
                accept_content_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{accept_content_datatestid}"]')))
                time.sleep(1)
                self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", accept_content_element)        
                accept_content_element.click()
            except NoSuchElementException:
                pass

            
            apply_to_the_job_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{apply_to_the_job_datatestid}"]')))
            time.sleep(0.5)
            self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", apply_to_the_job_element)
            apply_to_the_job_element.click()
            time.sleep(wait_time)

            try:
                apply_to_the_job_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{apply_to_the_job_datatestid}"]')))
                print("Cover letter needed")
            except NoSuchElementException:
                print("Apply went well")
                pass
        except:
            traceback.print_exc()

        
def apply_script(question_mode=False):
    """Script that will do the apply"""
    auto_apply = ApplyBot()
    auto_apply.question_mode=question_mode
    print(f"question_mode {question_mode}")
    if question_mode:
        auto_apply.number_of_page_to_search = 10
        auto_apply.maximum_number_of_offer = 999

    # 1 Login

    if auto_apply.login() is False:
        print("Login Failed goodbye")
        return
    
    # 2 Search job offers

    #auto_apply.search_job_offers()
    auto_apply.list_of_job_url = ["https://www.welcometothejungle.com/fr/companies/margo/jobs/developpeur-python-r-d-h-f_paris_MARGO_QbXxgjl","https://www.welcometothejungle.com/fr/companies/keyrus/jobs/developpeur-euse-python-h-f-nb-paris_levallois"]
    print(auto_apply.list_of_job_url)

    # 3 Parse job offers

    for job_offer in auto_apply.list_of_job_url:
        auto_apply.parse_job_offer(job_offer)
        time.sleep(11000)
    
    # send_message_discord(f"Hello the bot have found today {len(auto_apply.list_of_job_url)} jobs offers \n {len(auto_apply.list_of_job_inside_welcome_to_the_jungle_url)} inside welcome to the jungle \n {len(auto_apply.list_of_job_outside_welcome_to_the_jungle_url)} outside welcome to the jungle")
    # for url in auto_apply.list_of_job_inside_welcome_to_the_jungle_url:
    #     send_message_discord(f"New job! {url}", discord_job_inside)
    # for url in auto_apply.list_of_job_outside_welcome_to_the_jungle_url:
    #     send_message_discord(f"New job! {url}", discord_job_outside)
    
    time.sleep(1000)

    # ? Cleanup file

    remove_doublon_from_list_of_question_file()