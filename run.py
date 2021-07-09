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

import mylib

# Download Dir
dir_path = os.path.abspath(os.getcwd())+'/download/'

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : dir_path}
chromeOptions.add_experimental_option("prefs",prefs)
chromedriver = "chromedriver"

driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

# Open the main page
driver.get("https://apps.ute.com.uy/SgePublico/BajadasGE.aspx")    

driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_optEmbalse").click()
time.sleep(2)
 
# ------------------------------------------------------------
# Filter To Date
cboAnioFin = '1994'
cboMesFin = 'Marzo'

# //*[@id="ctl00_ContentPlaceHolder1_cboAnioFin"]
mylib.drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboAnioFin", option_value=cboAnioFin, driver=driver)
mylib.drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboMesFin", option_value=cboMesFin, driver=driver)


# ------------------------------------------------------------
# Filter From Date
cboAnioIni = '1994'
cboMesIni = 'Enero'

# //*[@id="ctl00_ContentPlaceHolder1_cboAnioIni"]
mylib.drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboAnioIni", option_value=cboAnioIni, driver=driver)
mylib.drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboMesIni", option_value=cboMesIni, driver=driver)

# ------------------------------------------------------------
# Download the file   
time.sleep(5)
driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_cmdDescargar").click()   