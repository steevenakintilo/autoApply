# Importing my chatgpt scrapper code to avoid recoding the same stuff for cover letter
# pylint: disable=all

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from random import randint
import undetected_chromedriver as uc 
import os
import yaml

class Scraper:
    
    wait_time = 5
    options = uc.ChromeOptions()
    options.add_experimental_option(
    "prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
    options.add_argument('headless')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    options.add_argument(f'--user-agent={ua}') 
    try:
      driver = uc.Chrome(options=options)
    except Exception as e:
      if "This version of ChromeDriver only supports Chrome version" in str(e):
        print("Update your chrome version!!!")
        print("https://www.google.com/intl/fr_fr/chrome/")
        exit()

    driver.maximize_window()
    login_link = "https://chat.openai.com/auth/login"
    emailxpath = "/html/body/div/main/section/div/div/div/div[1]/div/form/div[1]/div/div/div/input"
    passwordxpath = "/html/body/div[1]/main/section/div/div/div/form/div[2]/div/div[2]/div/input"
    continuexpath = "/html/body/div/main/section/div/div/div/div[1]/div/form/div[2]/button"
    continuexpath2 = "/html/body/div[1]/main/section/div/div/div/form/div[3]/button"
    mainpage = "https://chat.openai.com/"
    askid = "prompt-textarea"
    has_asked_question = False
    chatgptanswer = "/html/body/div[1]/div[1]/div/main/div[1]/div[1]/div/div/div/div[3]/div/div/div[2]/div[2]/div[1]"
    question_nb = 3
    btn_there = "/html/body/div[1]/div[1]/div/main/div[1]/div[1]/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div"
    dodo  = "/html/body/div[1]/div[1]/div/main/div[1]/div[1]/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div/button[1]/svg"
    d = "icon-md"
    with open("configuration.yml", "r") as file:
      data = yaml.load(file, Loader=yaml.FullLoader)
    
     

def maker(questions):
    S =  Scraper()
    ans_list = []
    questions_list = ["what is chatgpt"] + questions
    for i in range(len(questions_list)):
      time.sleep(1)
      ans = while_loop(S,questions_list[i])
      ans_list.append(ans)
    try:
      S.driver.close()
    except:
      return ""
    return ans_list[1:]


def while_loop(S,q):
  q = q.replace("\n" , " ")
  query = q
  answer = scrapping(S,query,"new",S.question_nb)
  return answer


# No need to login to google an account so we skip this function

def scrapping(S, query,mode,nb,stop=0):
    if stop >= 3:
      #print("Too many errors happend closing ScrapGPT")
      try:
        S.driver.close()
      except:
        return ""

      return ""
    
    try:
      S.driver.get(S.mainpage)
    except:
      time.sleep(5)
      S.driver.get(S.mainpage)
      time.sleep(5)
      S.driver.refresh()      
    time.sleep(5)


    try:
      accept_cookies_xpath_element = WebDriverWait(S.driver,5).until(
      EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/button[3]")))
      accept_cookies_xpath_element.click()
      time.sleep(5)
    except:
      pass

    if nb > 0:
      nb = nb - 1
    
    try:
      stay_logout_xpath = "/html/body/div[4]/div/div/div/div/div/a"
      element = WebDriverWait(S.driver, 5).until(
      EC.presence_of_element_located((By.XPATH, stay_logout_xpath)))
      time.sleep(2)
      element.click()
      time.sleep(2)
    except:
      pass
    time.sleep(1)
    S.driver.refresh()
    time.sleep(2.5)
    time.sleep(2.5)
    actions = ActionChains(S.driver)
    actions.send_keys(query).perform()
    actions.send_keys(Keys.RETURN).perform()
    time.sleep(10)
    
    for i in range(25):
      get_url = S.driver.current_url
      if "https://chat.openai.com/auth/login" in get_url:
        #print("Wrong email or password change it on configuration.yml file")
        try:
          S.driver.close()
        except:
          return ""

        return ""
      try:
        element = S.driver.find_element(By.XPATH, '[data-testid="stop-button"]')
        time.sleep(12)
      except Exception as e:
        pass
    try:
      try:
        element = WebDriverWait(S.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="conversation-turn-{nb}"]')))
        answer = S.driver.find_element(By.CSS_SELECTOR,f'[data-testid="conversation-turn-{nb}"]')
        answer = answer.text
        return (answer.replace("ChatGPT",""))
      except:
          element = WebDriverWait(S.driver, 5).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="conversation-turn-{nb+1}"]')))
          answer = S.driver.find_element(By.CSS_SELECTOR,f'[data-testid="conversation-turn-{nb+1}"]')
          answer = answer.text
          return (answer.replace("ChatGPT",""))
    except Exception as e:
      if stop >= 3:
        return ""
      if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
        #print("No connection sleeping for 30 secondes")
        time.sleep(30)
        stop+=1
        scrapping(S,query,mode,nb,stop)
      elif "element = WebDriverWait(S.driver, 9).until(" in str(e):
        time.sleep(15)
        stop+=1
        stop+=1
        scrapping(S,query,mode,nb,stop)
      else:
        #print("An error happend try again")
        stop+=1
        scrapping(S,query,mode,nb,stop)
        try:
          S.driver.close()
        except:
          return ""
      
        try:
          S.driver.close()
        except:
          return ""