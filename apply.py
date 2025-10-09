"""File that handle all the apply process"""

# pylint: disable=C0301
# pylint: disable=W0702

from datetime import date
from random import randint

import pickle
import time
import traceback
import yaml

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utility_function import *
from global_variable import *
from scrap import *
from gpt import GptScraper

class Scrapper():
    """Selenium window class"""
    wait_time:int = 5
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=1')
    options.add_argument("--log-level=3")
    # if len(str(print_pkl_info())) > 20:
    #     options.add_argument('headless')

    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(15)

class ApplyBot():
    "ApplyBot class"
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
        self.where_is_the_job:list[str] = self.configuration_file_data["where_is_the_job"]
        self.language:str = self.configuration_file_data["language"]
        self.resume_text:str = print_file_content("resume_text.txt")
        self.covert_letter_lenght:str = self.configuration_file_data["covert_letter_lenght"]
        self.forbiden_words_job_offer_question:list[str] = self.configuration_file_data["forbiden_words_job_offer_question"]
        self.forbiden_words_job_offer_text:list[str] = self.configuration_file_data["forbiden_words_job_offer_text"]
        self.skip_question:bool = self.configuration_file_data["skip_question"]
        self.skip_cover_letter:bool = self.configuration_file_data["skip_cover_letter"]
        self.print_error:bool = self.configuration_file_data["print_error"]
        self.list_of_job_url_to_retry:list[str] = []
        self.apply_good:int = 0
        self.apply:bool = self.configuration_file_data["apply"]
        self.list_of_job_url_question_to_answer:list[str] = []
        self.list_of_applied_job:list[str] = print_file_content("list_of_questions.txt").lower().split("\n")
        self.list_of_job_question_answered:list[str] = print_file_content("list_of_job_question_answered.txt").lower().split("\n")
        self.country_of_the_job:str = self.configuration_file_data["country_of_the_job"]
        self.apply_to_offer_who_have_job_keyword_list_element_in_their_name:bool = self.configuration_file_data["apply_to_offer_who_have_job_keyword_list_element_in_their_name"]
        self.print_cover_letter:bool = self.configuration_file_data["print_cover_letter"]
        self.bad_apply:int = 0
        self.skipped_apply:int = 0
        self.forbiden_words_job_offer_name = self.configuration_file_data["forbiden_words_job_offer_name"]

    def login(self) -> bool:
        """Login to Welcome to the jungle"""
        try:
            self.scrapping_window.driver.get(login_page_url)
            time.sleep(wait_time2)
            if len(str(self.cookies_file_data)) > 10:
                cookies = pickle.load(open("cookies.pkl","rb"))
                button_to_triger_login_page_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{button_to_triger_login_page_datatestid}"]')))
                button_to_triger_login_page_element.click()
                time.sleep(wait_time2)
                for cookie in cookies:
                    self.scrapping_window.driver.add_cookie(cookie)
                return True

            button_to_triger_login_page_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{button_to_triger_login_page_datatestid}"]')))
            button_to_triger_login_page_element.click()
            time.sleep(wait_time)
            login_button_email_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{login_button_email_datatestid}"]')))
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
            time.sleep(wait_time2)
            try:
                accept_cookies_xpath_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.XPATH, accept_cookies_xpath)))
                accept_cookies_xpath_element.click()
                time.sleep(wait_time2)
            except:
                pass
            time.sleep(wait_time2)
            try:
                accept_cookies_xpath_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.XPATH, accept_cookies_xpath2)))
                accept_cookies_xpath_element.click()
                time.sleep(wait_time2)
            except:
                pass
            time.sleep(wait_time2)
            try:
                accept_cookies_xpath_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.ID, accept_cookies_id)))
                accept_cookies_xpath_element.click()
                time.sleep(wait_time2)
            except:
                pass
            pickle.dump(self.scrapping_window.driver.get_cookies(), open("cookies.pkl", "wb"))
            time.sleep(wait_time2)
            return True
        except Exception as e:
            if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
                if self.print_error:
                    print("No connection sleeping for 5 minutes")
                time.sleep(300)
            if self.print_error:
                traceback.print_exc()
            return False


    def search_job_offers(self) -> None:
        """Searching job offer"""
        try:
            grid = False
            sort_by = sort_by_relevance
            if self.sort_job_by_date:
                sort_by = sort_by_date
            job_type = permanent_job_url_typing
            if self.is_intership:
                job_type = internship_job_url_typing
            for words in self.job_keyword_list:
                localisation_of_the_job = ""
                current_job_page = f"{job_page_url}{convert_list_to_correct_url_typing(words)}{job_type}{localisation_of_the_job}{sort_by}"
                if len(self.list_of_job_url) >= self.maximum_number_of_offer:
                    break
                try:
                    self.scrapping_window.driver.get(current_job_page)
                    time.sleep(2)
                except:
                    self.scrapping_window.driver.get(current_job_page)
                    self.scrapping_window.driver.refresh()
                    time.sleep(wait_time3)
                
                if grid is False:
                    grid_view_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                    EC.presence_of_element_located((By.XPATH, grid_view_xpath)))
                    grid_view_element.click()
                    grid = True
                    time.sleep(wait_time2)
                    
                self.current_url = current_job_page
                for page_number in range(self.number_of_page_to_search):
                    print(f"{words} page number: {page_number + 1} number of jobs found {len(self.list_of_job_url)}")
                    job_offer_localisation_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{job_offer_localisation_datatestid}"]')))
                    if job_offer_localisation_element.text.lower() != self.country_of_the_job.lower() and page_number == 0:
                        try:
                            self.scrapping_window.driver.execute_script("arguments[0].click();", job_offer_localisation_element)
                            time.sleep(1)
                            job_offer_localisation_element.send_keys(Keys.CONTROL, 'a')
                            job_offer_localisation_element.send_keys(Keys.BACKSPACE)
                            job_offer_localisation_element.send_keys(self.country_of_the_job)
                            time.sleep(1)
                            try:
                                job_offer_first_localisation_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                                EC.presence_of_element_located((By.XPATH, job_offer_first_localisation_xpath)))
                                self.scrapping_window.driver.execute_script("arguments[0].click();", job_offer_first_localisation_element)
                                time.sleep(wait_time2)
                            except:
                                job_offer_first_localisation_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                                EC.presence_of_element_located((By.XPATH, job_offer_first_localisation_xpath2)))
                                self.scrapping_window.driver.execute_script("arguments[0].click();", job_offer_first_localisation_element)
                                time.sleep(wait_time2)
                        except:
                            if self.print_error:
                                traceback.print_exc()
                                time.sleep(1)
                            self.scrapping_window.driver.get(current_job_page)
                            time.sleep(wait_time2)
                    
                    if len(self.list_of_job_url) >= self.maximum_number_of_offer:
                        break
                    if page_number != 0:
                        time.sleep(wait_time2)
                        try:
                            self.scrapping_window.driver.get(f"{current_job_page}{sort_by}&page={str(page_number+1)}{localisation_of_the_job}")
                            time.sleep(wait_time)                            
                        except:
                            self.scrapping_window.driver.get(f"{current_job_page}{sort_by}&page={str(page_number+1)}{localisation_of_the_job}")
                            self.scrapping_window.driver.refresh()
                            time.sleep(wait_time3)
                    self.get_job_info_by_page()
        except Exception as e:
            if self.print_error:
                traceback.print_exc()
            if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
                if self.print_error:
                    print("No connection sleeping for 5 minutes")
                time.sleep(300)


    def get_job_info_by_page(self) -> None:
        """Getting all jobs info of each page"""
        try:
            all_jobs_of_the_page_element  = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'[data-testid="{all_jobs_of_the_page_datatestid}"]')))
        except Exception as e:
            if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
                if self.print_error:
                    print("No connection sleeping for 5 minutes")
                time.sleep(300)
            time.sleep(wait_time2)
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
                    if len(str(current_job_url_element.get_property("href"))) > 5:
                        write_into_file("all_job_url.txt", current_job_url_element.get_property("href") + "\n")
                time.sleep(0.2)
                self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", current_job_url_element)
                index+=1
            except Exception as e:
                if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
                    if self.print_error:
                       print("No connection sleeping for 5 minutes")
                    time.sleep(300)

                try:
                    profile_dissmiss_button_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{profile_dissmiss_button_datatestid}"]')))
                    profile_dissmiss_button_element.click()
                    index-=1
                except:
                    if self.print_error:
                        traceback.print_exc()

    def parse_and_apply_to_job_offer(self,job_offer_url,):
        """Parsing job offer then apply"""
        try:
            today = date.today()
            if job_offer_url.lower() in self.list_of_applied_job:
                return
            if self.question_mode is True and job_offer_url.lower() in self.list_of_job_question_answered:
                return
            skip = False
            list_of_question:list[str] = []
            cant_apply_job_list:list[str] = []
            self.list_of_questions_find:list[str] = print_file_content("list_of_questions.txt").lower().split("\n")
            time.sleep(2)
            try:
                self.scrapping_window.driver.get(job_offer_url)
                time.sleep(1)
            except:
                self.scrapping_window.driver.get(job_offer_url)
                self.scrapping_window.driver.refresh()
                time.sleep(wait_time3)
            
            info_of_the_job_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{info_of_the_job_datatestid}"]')))

            try:
                good_town = False
                for town in self.where_is_the_job:
                    if town.lower() in info_of_the_job_element.text.lower():
                        good_town = True
            except TypeError:
                good_town = True
            
            if "anywhere" in self.where_is_the_job or "anywhere" in str(self.where_is_the_job):
                good_town = True
            
            if self.question_mode:
                good_town = True
            if good_town is False:
                send_message_discord(f"Can't apply to this job because the job offer is not from a city you provided {job_offer_url}",discord_job_banned)
                write_into_file("wrong_town.txt",job_offer_url)
                self.skipped_apply+=1
                return
            try:
                apply_button_data_testid_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{apply_button_data_testid}"]')))

            except:
                if job_offer_url not in self.list_of_job_url_to_retry:
                    self.list_of_job_url_to_retry.append(job_offer_url)
                return

            if apply_button_data_testid_element.get_property("href") is not None:
                self.list_of_job_outside_welcome_to_the_jungle_url.append(job_offer_url)
                return

            self.list_of_job_inside_welcome_to_the_jungle_url.append(job_offer_url)
            apply_button_data_testid_element.click()
            time.sleep(wait_time2)

            if self.apply_to_offer_who_have_job_keyword_list_element_in_their_name:
                try:
                    job_offer_name_element = WebDriverWait(self.scrapping_window.driver,wait_time).until(
                    EC.presence_of_element_located((By.XPATH, job_offer_name_xpath)))
                    if are_words_inside_list_of_words(job_offer_name_element.text,self.job_keyword_list) is False:
                        send_message_discord(f"Can't apply to this job because the job offer name '{job_offer_name_element.text}' isn't inside job_keyword_list {str(self.job_keyword_list)}{job_offer_url}",discord_job_banned)
                        self.skipped_apply+=1
                        self.list_of_job_url_question_to_answer.append(job_offer_url)
                        return

                except:
                    pass

                try:
                    for forbiden_word in self.forbiden_words_job_offer_name:
                        for word in str(self.forbiden_words_job_offer_name).split(" "):
                            if forbiden_word.lower() == word.lower() and self.question_mode is False:
                                send_message_discord(f"Can't apply to this job because there is a forbiden word '{forbiden_word}' inside job offer name {job_offer_url}",discord_job_banned)
                                self.skipped_apply+=1
                                return
                except TypeError:
                    pass
                

            #print(apply_form_text_split)
            # Searching for job name:
            if self.question_mode is False:
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


            try:
                for forbiden_word in self.forbiden_words_job_offer_text:
                    for word in str(self.forbiden_words_job_offer_text).split(" "):
                        if forbiden_word.lower() == word.lower() and self.question_mode is False:
                            send_message_discord(f"Can't apply to this job because there is a forbiden word '{forbiden_word}' inside job offer text {job_offer_url}",discord_job_banned)
                            self.skipped_apply+=1
                            return
            except TypeError:
                pass
            
            apply_form_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{apply_form_datatestid}"]')))
            if self.question_mode is False:
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
                except:
                    pass

            # Searching for question
            try:
                job_offer_xpath_nb = 999

                for i , job_xpath in enumerate(job_offer_question_xpath_list):
                    try:
                        job_offer_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 7).until(
                        EC.presence_of_element_located((By.XPATH, job_xpath)))
                        job_offer_xpath_nb = i
                        #print(job_xpath)
                    except:
                        pass
                question_word_found = False
                for question_translation in question_in_several_language_list:
                    if question_translation.lower() in str(apply_form_element.text.lower()):
                        question_word_found = True
                # if job_offer_xpath_nb == 999 and question_word_found is False and self.question_mode:
                #     print("no question on this offer " , job_offer_url)
                #     write_into_file("list_of_job_question_answered.txt",job_offer_url+"\n")

                if job_offer_xpath_nb != 999 or question_word_found:
                    if self.skip_question:
                        send_message_discord(f"Can't apply to this job because you choose to skip job where a question is needed {job_offer_url}",discord_job_banned)
                        self.skipped_apply+=1
                        return
                    
                    if job_offer_xpath_nb < 0:
                        job_offer_xpath_nb = 0
                    try:
                        list_of_question = job_offer_question_element.text.split("\n")[1:]
                    except:
                        list_of_question = []
                    
                    # if len(list_of_question) == 0:
                    #     print("check question xpath for this offer: " , job_offer_url)
                    #     write_into_file("check_question_xpath.txt",job_offer_url+"\n")

                    try:
                        for forbiden_word in self.forbiden_words_job_offer_question:
                            for question in list_of_question:
                                for word in question.split(" "):
                                    if forbiden_word.lower() == word.lower():
                                        send_message_discord(f"Can't apply to this job because there is a forbiden word '{forbiden_word}' inside job offer question {job_offer_url}",discord_job_banned)
                                        self.skipped_apply+=1
                                        return
                    except TypeError:
                        pass
                    if self.question_mode:
                        write_into_file("list_of_job_question_answered.txt",job_offer_url+"\n")
                        for index , text in enumerate(list_of_question):
                            try:
                                current_question_xpath = f"/html/body/div[{job_offer_question_xpath_list_special_nb[job_offer_xpath_nb]}]/div[2]/div/section/form/fieldset[3]/div[{str(index + 1)}]/div/textarea"
                                current_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                                EC.presence_of_element_located((By.XPATH, current_question_xpath)))
                            except:
                                try:
                                    current_question_xpath = f"/html/body/div[{job_offer_question_xpath_list_special_nb[job_offer_xpath_nb]}]/div[2]/div/section/form/fieldset[3]/div/div/div[2]/div[1]/div[1]"
                                    current_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                                    EC.presence_of_element_located((By.XPATH, current_question_xpath)))
                                except:
                                    current_question_xpath = f"/html/body/div[{job_offer_question_xpath_list_special_nb[job_offer_xpath_nb]}]/div[2]/div/section/form/fieldset[3]/div/div/div[{str(index + 1)}]/div[1]/div[1]"
                                    current_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                                    EC.presence_of_element_located((By.XPATH, current_question_xpath)))


                            current_question_element.click()
                            if "choose" in current_question_element.get_attribute("placeholder").lower():
                                send_message_discord(f"Can't apply to this job because it's a placeholder and not question {job_offer_url}",discord_job_error)
                                self.skipped_apply+=1
                                return
                            time.sleep(1)
                            self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", current_question_element)
                            time.sleep(2)

                            if len(text) > 5:
                                if "'!'" in str(list_of_question):
                                    return
                                if text.lower() not in str(self.list_of_questions) and text.lower() not in self.list_of_questions_find:
                                    #print(text,job_offer_url)
                                    print("Question found:" , text , job_offer_url)
                                    send_message_discord("Question found: " + text , job_offer_url)
                                    write_into_file("list_of_questions.txt",text.lower()+"#####"+"\n")
                                    self.list_of_questions.append(text.lower())

                        #print(apply_form_datatestid_element.text)
                        #print(job_offer_url)
                        #print(".........")
                    else:
                        for index , text in enumerate(list_of_question):
                            try:
                                for forbiden_word in self.forbiden_words_job_offer_question:
                                    if forbiden_word.lower() in text.lower():
                                        send_message_discord(f"Can't apply to this job because there is a forbiden word inside job question: {forbiden_word} {job_offer_url}",discord_job_banned)
                                        self.skipped_apply+=1
                                        return
                            except TypeError:
                                pass
                            try:
                                current_question_xpath = f"/html/body/div[{job_offer_question_xpath_list_special_nb[job_offer_xpath_nb]}]/div[2]/div/section/form/fieldset[3]/div[{str(index + 1)}]/div/textarea"
                                current_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                                EC.presence_of_element_located((By.XPATH, current_question_xpath)))
                            except:
                                try:
                                    current_question_xpath = f"/html/body/div[{job_offer_question_xpath_list_special_nb[job_offer_xpath_nb]}]/div[2]/div/section/form/fieldset[3]/div/div/div[2]/div[1]/div[1]"
                                    current_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                                    EC.presence_of_element_located((By.XPATH, current_question_xpath)))
                                except:
                                    current_question_xpath = f"/html/body/div[{job_offer_question_xpath_list_special_nb[job_offer_xpath_nb]}]/div[2]/div/section/form/fieldset[3]/div/div/div[{str(index + 1)}]/div[1]/div[1]"
                                    current_question_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                                    EC.presence_of_element_located((By.XPATH, current_question_xpath)))


                            current_question_element.click()
                            if "choose" in current_question_element.get_attribute("placeholder").lower():
                                send_message_discord(f"Can't apply to this job because it's a placeholder and not question {job_offer_url}",discord_job_error)
                                self.skipped_apply+=1
                                return
                            time.sleep(1)
                            self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", current_question_element)
                            time.sleep(2)
                            if len(text) > 5:
                                if text.lower() not in str(self.list_of_questions_find):
                                    write_into_file("list_of_questions.txt",text.lower()+"#####"+"\n")
                                    self.list_of_questions.append(text.lower())
                                    send_message_discord(f"Answer and add this question to all_questions.txt file with the answer\n {text} {job_offer_url}", discord_question)
                                    self.list_of_job_url_question_to_answer.append(job_offer_url.lower())
                                    skip = True

                                if skip is False:
                                    answer = get_answer_from_question_list(text)
                                    if (answer == "skip" or "skip" in answer):
                                        send_message_discord(f"Can't apply to this job because I don't want to answer the questions {job_offer_url}",discord_job_banned)
                                        self.skipped_apply+=1
                                        return
                                    if answer == ""  or answer == "_answer_error_":
                                        send_message_discord(f"Can't apply to this job because I don't have answer to the question {text} {job_offer_url}",discord_question)
                                        self.skipped_apply+=1
                                        self.list_of_job_url_question_to_answer.append(job_offer_url)
                                        return
                                    try:
                                        current_question_element.clear()
                                    except:
                                        send_message_discord(f"Can't apply to this job because there is info to check but not question {job_offer_url}",discord_job_error)
                                        self.skipped_apply+=1
                                        return
                                    time.sleep(0.5)
                                    current_question_element.send_keys(answer)
                                
            except:
                if self.print_error:
                    pass
                    # traceback.print_exc()
                    # print("Error part 2")
                    # traceback.print_exc()
                    # print(job_offer_url)
                    # print(list_of_question)
            if skip:
                return
            # Accept consent

            if self.question_mode is False:
                try:
                    accept_content_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{accept_content_datatestid}"]')))
                    time.sleep(1)
                    self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", accept_content_element)
                    accept_content_element.click()
                except:
                    pass

            if self.question_mode is False:
                apply_to_the_job_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{apply_to_the_job_datatestid}"]')))
                time.sleep(0.5)
                self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", apply_to_the_job_element)
                apply_to_the_job_element.click()
                time.sleep(wait_time)

                skip_cover = False
                try:
                    accept_content_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{accept_content_datatestid}"]')))
                    time.sleep(1)
                except:
                    skip_cover = True
                
                try:
                    if skip_cover is False:
                        apply_to_the_job_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{apply_to_the_job_datatestid}"]')))

                        #print("Cover letter needed")
                        
                        if self.skip_cover_letter:
                            send_message_discord(f"Can't apply to this job because you choose to skip job where a cover letter is needed {job_offer_url}",discord_job_banned)
                            return
                        question_to_ask_to_chatgpt = f"From my resume and the text of this job offer can you generate a {self.covert_letter_lenght} cover letter without mentioning the subject of the cover letter the city or the date of the day and just put the text of the cover letter without adding your own opinions/texts and be humble and personal in the cover letter generate the text in {self.language}   {self.resume_text} \n job description:\n {job_offer_text_element.text} just return the cover letter don't add your own text or thinking just the text of the cover letter!!!"
                        
                        try:
                            chatgpt = GptScraper()
                            chatgpt.maker([question_to_ask_to_chatgpt])
                            cover_letter_text = chatgpt.answer_list[0]
                        except:
                            if self.print_error:
                                traceback.print_exc()
                            if job_offer_url not in self.list_of_job_url_to_retry:
                                self.list_of_job_url_to_retry.append(job_offer_url)
                                return
                            elif job_offer_url in self.list_of_job_url_to_retry and self.question_mode is False:  
                                send_message_discord(f"Apply error on this job offer because of the cover letter generation{job_offer_url}",discord_job_error)
                                self.bad_apply+=1
                                write_into_file("error_job_url.txt",job_offer_url)
                                return
                        if len(str(cover_letter_text)) < 30:
                            if job_offer_url in self.list_of_job_url_to_retry:
                                send_message_discord(f"Apply error on this job offer {job_offer_url} because the bot failed to generate the cover letter",discord_job_error)
                                self.bad_apply+=1
                                write_into_file("error_job_url.txt",job_offer_url+"\n")
                            elif job_offer_url not in self.list_of_job_url_to_retry:
                                self.list_of_job_url_to_retry.append(job_offer_url)
                            return

                        if self.print_cover_letter:
                            send_message_discord(f"Generated Cover Letter:\n {cover_letter_text} \n link of the job offer: {job_offer_url}",discord_cover_letter)
                            self.list_of_job_url_question_to_answer.append(job_offer_url)
                            return
                                            
                        if len(str(cover_letter_text)) > 30:
                            cover_letter_element = WebDriverWait(self.scrapping_window.driver,wait_time - 6).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{cover_letter_datatestid}"]')))
                            time.sleep(0.5)
                            self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", cover_letter_element)
                            time.sleep(1)
                            cover_letter_element.send_keys(cover_letter_text)
                            time.sleep(8)
                            self.scrapping_window.driver.execute_script("arguments[0].scrollIntoView();", apply_to_the_job_element)
                            time.sleep(0.5)
                            apply_to_the_job_element.click()
                            time.sleep(2)

                except:
                    if self.print_error:
                        traceback.print_exc()
            #print("well done")

            try:
                apply_to_the_job_element = WebDriverWait(self.scrapping_window.driver,wait_time - 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{apply_to_the_job_datatestid}"]')))
                if job_offer_url not in self.list_of_job_url_to_retry:
                    self.list_of_job_url_to_retry.append(job_offer_url)
                elif job_offer_url in self.list_of_job_url_to_retry and self.question_mode is False:  
                    send_message_discord(f"Apply error on this job offer {job_offer_url}",discord_job_error)
                    self.bad_apply+=1
                    write_into_file("error_job_url.txt",job_offer_url)
            except:
                pass

            if self.question_mode is False:
                write_into_file("list_of_applied_job.txt" , job_offer_url.lower() + "\n")
                write_into_file("list_of_applied_job_date.txt" , str(today.strftime("%d/%m/%Y")) + " " + job_offer_url.lower() + "\n")
                send_message_discord(f"I have applied to this job offer! {job_offer_url}" , discord_apply_sucess)
                if len(list_of_question) == 0:
                    time.sleep(randint(1,20))
            self.apply_good+=1
        except Exception as e:
            if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
                if self.print_error:
                    print("No connection sleeping for 5 minutes")
                if job_offer_url in self.list_of_job_url_to_retry and self.question_mode is False:  
                    send_message_discord(f"Apply error on this job offer {job_offer_url} because they were no wifi",discord_job_error)
                time.sleep(300)

            if self.print_error:
                traceback.print_exc()      
            if job_offer_url not in self.list_of_job_url_to_retry:
                self.list_of_job_url_to_retry.append(job_offer_url)
            elif job_offer_url in self.list_of_job_url_to_retry and self.question_mode is False:  
                send_message_discord(f"Apply error on this job offer {job_offer_url}",discord_job_error)
                write_into_file("error_job_url.txt",job_offer_url)
                self.bad_apply+=1


def apply_script(question_mode=False):
    """Script that will do the apply"""
    auto_apply = ApplyBot()
    auto_apply.question_mode=question_mode
    if question_mode:
        auto_apply.number_of_page_to_search = 10
        auto_apply.maximum_number_of_offer = 999

    # 1 Login
    
    if auto_apply.login() is False:
        print("Login Failed goodbye")
        return

    # 2 Search job offers

    auto_apply.search_job_offers()

    #auto_apply.list_of_job_url = ["https://www.welcometothejungle.com/fr/companies/altametris/jobs/developpeur-euse-polyvalent-e-image-3d-cloud"]
    if question_mode is False:

        # 3 If auto apply exit program
        if auto_apply.apply is False:
            send_message_discord("No need to apply see you soon",discord_stat)
            return
        
        # 4 Parse job offers then apply
        if auto_apply.apply:
            for index , job_offer in enumerate(auto_apply.list_of_job_url):
                print(f"Job offer {index+1}/{len(auto_apply.list_of_job_url)} url:{job_offer}")
                auto_apply.parse_and_apply_to_job_offer(job_offer)

        # 5 Send offer link to discord
        
        send_message_discord("-"*50,discord_job_inside)
        send_message_discord("-"*50,discord_job_outside)
        send_message_discord("-"*50,discord_job_error)
        send_message_discord("-"*50,discord_job_banned)
        
        if len(auto_apply.list_of_job_url) == 0:
            send_message_discord("The bot have found 0 job offer maybe try to change the configuration.yml to find more job such as more jobs into job_keyword_list or more town inside where_is_the_job...")
        for url in auto_apply.list_of_job_inside_welcome_to_the_jungle_url:
            if url not in auto_apply.list_of_job_inside_welcome_to_the_jungle_url:
                send_message_discord(f"New job! {url}", discord_job_inside)
                write_into_file("list_of_jobs_inside_welcome_to_the_jungle.txt",url+"\n")
        for url in auto_apply.list_of_job_outside_welcome_to_the_jungle_url:
            if url not in auto_apply.list_of_job_outside_welcome_to_the_jungle_url:
                send_message_discord(f"New job! {url}", discord_job_outside)
                write_into_file("list_of_jobs_outside_welcome_to_the_jungle.txt",url+"\n")

        #  6 Trying to apply again of job offer that failed
        
        list_of_all_job_applied_url = print_file_content("list_of_applied_job.txt").lower().split("\n")
        for index , job_offer_url_to_retry in enumerate(auto_apply.list_of_job_url_to_retry):
            if job_offer_url_to_retry.lower() not in list_of_all_job_applied_url:
                print(f"Job offer retry {index+1}/{len(auto_apply.list_of_job_url_to_retry)} url:{job_offer_url_to_retry}")
                auto_apply.parse_and_apply_to_job_offer(job_offer_url_to_retry)
    else:
        for index , job_offer in enumerate(auto_apply.list_of_job_url):
            print(f"Job offer question looking {index+1}/{len(auto_apply.list_of_job_url)} url:{job_offer}")
            auto_apply.parse_and_apply_to_job_offer(job_offer)

    # 7 Cleanup file

    remove_doublon_from_list_of_question_file()
    list_of_all_job_url = print_file_content("all_job_url.txt").lower().split("\n")
    
    reset_file("all_job_url.txt")

    for job_url in list_of_all_job_url:
        if job_url.lower() not in auto_apply.list_of_job_url_question_to_answer and len(job_url) > 5:
            write_into_file("all_job_url.txt",job_url.lower()+"\n")

    # 8 Bye bye
    outside_verb = "was"
    skipped_verb = "was"

    skipped_nb = (len(auto_apply.list_of_job_url) -  (auto_apply.apply_good + len(auto_apply.list_of_job_outside_welcome_to_the_jungle_url) + auto_apply.bad_apply))
    if skipped_nb < 0:
        skipped_nb = 0
    if len(auto_apply.list_of_job_outside_welcome_to_the_jungle_url) > 1:
        outside_verb = "were"
    if skipped_nb > 1:
        skipped_verb = "were"

    if question_mode is False:
        send_message_discord(f"Among the {len(auto_apply.list_of_job_url)} jobs found:\n {auto_apply.apply_good} went well ✅ \n {len(auto_apply.list_of_job_outside_welcome_to_the_jungle_url)} {outside_verb} outside welcome to the jungle 🟦 \n {auto_apply.skipped_apply} {skipped_verb} skipped 🟧 \n {auto_apply.bad_apply} went bad ❌",discord_stat)
        send_message_discord("-"*50,discord_stat)
        print(f"Among the {len(auto_apply.list_of_job_url)} jobs found:\n {auto_apply.apply_good} went well ✅ \n {len(auto_apply.list_of_job_outside_welcome_to_the_jungle_url)} {outside_verb} outside welcome to the jungle 🟦 \n {skipped_nb} {skipped_verb} skipped 🟧 \n {auto_apply.bad_apply} went bad ❌")
        print("-"*50)
    if question_mode:
        print("Answer to the question inside list_of_questions.txt file")

    print("Good bye")
