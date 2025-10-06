# Importing my chatgpt scrapper code to avoid recoding the same stuff for cover letter
# pylint: disable=all

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from random import randint
import undetected_chromedriver as uc 

class Scraper:
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