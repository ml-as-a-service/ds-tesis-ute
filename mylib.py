from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

import time 
import os
import mylib
import json

def drowpdown_select(el_id, option_value, driver):
    xpath = '//*[@id="'+str(el_id)+'"]/option[. ="'+str(option_value)+'"]'
    # print('xpath', xpath)
    option = driver.find_element(By.XPATH, xpath)
    option.click()
    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.ID, el_id)))    

def file_put_contents(filename, content):
    with open(filename, 'w') as f_in: 
        f_in.write(content)

def file_get_contents(filename):
    with open(filename, 'r') as f_in: 
        return f_in.read()


def mydownload(driver, cboAnioIni,cboMesIni, cboAnioFin,cboMesFin):
    # ------------------------------------------------------------
    # Filter To Date
    # cboAnioFin = '1994'
    # cboMesFin = 'Marzo'

    # //*[@id="ctl00_ContentPlaceHolder1_cboAnioFin"]
    drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboAnioFin", option_value=cboAnioFin, driver=driver)
    drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboMesFin", option_value=cboMesFin, driver=driver)


    # ------------------------------------------------------------
    # Filter From Date
    # cboAnioIni = '1994'
    # cboMesIni = 'Enero'

    # //*[@id="ctl00_ContentPlaceHolder1_cboAnioIni"]
    drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboAnioIni", option_value=cboAnioIni, driver=driver)
    drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboMesIni", option_value=cboMesIni, driver=driver)

    # ------------------------------------------------------------
    # Download the file   
    time.sleep(2)
    # driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_cmdDescargar").click()  
    print('bajarmos............')




# --------------------------------------------------------------------
def process(d, level, path, paths):
    items = ['cuencas', 'subcuencas', 'estaciones', 'pasos']

    if(level != len(items)):  
        current = d[items[level]]
        for subtype, item in current.items(): #BAYGO 
            _path = path +','+subtype # +'('+current[subtype]['name']+')'
            # print(_path)
            paths.append(_path)
            process(current[subtype], level+1, _path, paths)

def dataJsonToCsv():
    dir_path = os.path.abspath(os.getcwd())+'/download/'
    file_data = dir_path+'/data.json'
    file_data_csv = dir_path+'/data.csv'

    data = mylib.file_get_contents(file_data) or {}
    data = json.loads(data)
            
    paths = []        
    process(data,0, 'new', paths)  # state: new, processing, done, error

    with open(file_data_csv, 'w') as f:
        f.write("estado,cuenca,subcuenca,estacion,paso\n" )
        for p in paths:
            if(p.count(',')>=4):
                f.write("%s\n" % p) #.replace('root,',''))    

