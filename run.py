import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
    
import os

# Download Dir
dir_path = os.path.abspath(os.getcwd())+'/download/'

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : dir_path}
chromeOptions.add_experimental_option("prefs",prefs)
chromedriver = "chromedriver"

driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

# Open the main page
driver.get("https://apps.ute.com.uy/SgePublico/BajadasGE.aspx")    
