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

import numpy as np

import pandas as pd
from datetime import datetime
from datetime import timedelta

def gen_estacion_latlon(file_name, file_name_out):
    dateparse = lambda x: datetime.strptime(x, '%d/%m/%Y') # %Y-%m-%d %H:%M:%S
    # 01/01/2000; 700; Central Baygorria; Directa Baygorria; Local Baygorria; El Monumento ;  ; 
    # file_name = 'download/ute/data/2000-Enero-2000-Junio-BAYGO-SDBAYGO-CPALMA-PTOROS.txt'
    # file_name_out = 'download/ute/csv/2000-Enero-2000-Junio-BAYGO-SDBAYGO-CPALMA-PTOROS.csv'

    # cuenca_id,cuenca_name,subcuenca_id,subcuenca_name,estacion_id,estacion_name,lat,lon,type
    file_data_lat_lon = "download/data_latlon.csv"
    df_lat_lon = pd.read_csv(file_data_lat_lon)
    df_lat_lon.drop(['cuenca_id','cuenca_name','subcuenca_id','subcuenca_name'], inplace=True, axis=1)

    col_names = ['date','hour','cuenca','subcuenca','x1','estacion','precipitacion','x2']
    df = pd.read_csv(file_name,
                    names=col_names,sep=";",skiprows=2,
                    parse_dates=["date"],date_parser=dateparse)

    df['dt'] = df['date'].astype(str) +' '+ df['hour'].apply(str).str[:-2] +':00:00' # pd.DateOffset(hours=df['hour']/100) #timedelta(2)
    df['dt'] = pd.to_datetime(df['dt'])

    # df['estacion'] = df['estacion'].str.strip()
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

    df.drop(['date','hour' ], inplace=True, axis=1)

    # export 
    df_estacion_latlon = df.join(df_lat_lon.set_index('estacion_name'),on="estacion")
    df_estacion_latlon.to_csv(file_name_out, index=False)


def drowpdown_select(el_id, option_value, driver):
    xpath = '//*[@id="'+str(el_id)+'"]'
    # print('xpath', xpath)
    option = driver.find_element(By.XPATH, xpath)
    val_option = option.get_attribute('text')

    if( val_option != option_value):
        xpath = '//*[@id="'+str(el_id)+'"]/option[. ="'+str(option_value)+'"]'
        # print('xpath', xpath)
        option = driver.find_element(By.XPATH, xpath)
        option.click()
        wait = WebDriverWait(driver, 20)
        wait.until(EC.element_to_be_clickable((By.ID, el_id)))   
        time.sleep(np.random.randint(3,5))  

def drowpdown_select_byvalue(el_id, option_value, driver):
    xpath = '//*[@id="'+str(el_id)+'"]'
    option = driver.find_element(By.XPATH, xpath)
    # print('xpath', xpath)
    val_option = option.get_attribute('value')

    if( val_option != option_value):
        xpath = '//*[@id="'+str(el_id)+'"]/option[@value="'+str(option_value)+'"]'
        option = driver.find_element(By.XPATH, xpath)
        option.click()
        wait = WebDriverWait(driver, 20)
        wait.until(EC.element_to_be_clickable((By.ID, el_id)))  
        time.sleep(np.random.randint(3,5))  


def file_put_contents(filename, content):
    with open(filename, 'w') as f_in: 
        f_in.write(content)

def file_get_contents(filename):
    with open(filename, 'r') as f_in: 
        return f_in.read()

def setTimeFilter(params):
    # print('setTimeFilter', params)
    driver = params['driver']      
    # ------------------------------------------------------------
    # Filter To Date
    cboAnioFin = params['cboAnioFin'] #'1994'
    cboMesFin = params['cboMesFin'] #'Marzo'

    # //*[@id="ctl00_ContentPlaceHolder1_cboAnioFin"]
    drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboAnioFin", option_value=cboAnioFin, driver=driver)
    drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboMesFin", option_value=cboMesFin, driver=driver)


    # ------------------------------------------------------------
    # Filter From Date
    cboAnioIni = params['cboAnioIni'] #'1994'
    cboMesIni = params['cboMesIni'] #'Enero'

    # //*[@id="ctl00_ContentPlaceHolder1_cboAnioIni"]
    drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboAnioIni", option_value=cboAnioIni, driver=driver)
    drowpdown_select(el_id="ctl00_ContentPlaceHolder1_cboMesIni", option_value=cboMesIni, driver=driver)



def setCuencaFilter(params):
    # print('setCuencaFilter', params)
    driver = params['driver'] 
    cuenca = params['cuenca'] 
    subcuenca = params['subcuenca'] 
    estacion = params['estacion'] 
    paso = params['paso']  

    # ------------------------------------------------------------
    # Download the file   
    time.sleep(np.random.randint(2,6))
    drowpdown_select_byvalue(el_id="ctl00_ContentPlaceHolder1_cboCuenca", option_value=cuenca, driver=driver)
    drowpdown_select_byvalue(el_id="ctl00_ContentPlaceHolder1_cboSubcuenca", option_value=subcuenca, driver=driver)
    drowpdown_select_byvalue(el_id="ctl00_ContentPlaceHolder1_cboEstacion", option_value=estacion, driver=driver)
    # remove paso filter #19
    # drowpdown_select_byvalue(el_id="ctl00_ContentPlaceHolder1_cboPasos", option_value=paso, driver=driver)
    
def download(driver):    
    print("Download File .....")
    time.sleep(np.random.randint(2,6))
    driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_cmdDescargar").click()  
    # TODO: REVISAR EN LA CARPTA DE DESCARGA SI HAY UN ARCHIVO MAS
    time.sleep(np.random.randint(5,15))
    




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

# https://www.codegrepper.com/code-examples/python/how+to+find+a+string+in+a+text+file+using+python
def search_string_in_file(file_name, string_to_search):
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results
