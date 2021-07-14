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

import numpy as np
import shutil
import glob 

dir = os.path.dirname(os.path.realpath(__file__))

# outfilename = dir+'/dist/extract_hierarchical_structure.js'

def file_put_contents(filename, content):
    with open(filename, 'w') as f_in: 
        f_in.write(content)

def file_get_contents(filename):
    with open(filename, 'r') as f_in: 
        return f_in.read()



# Download Dir
dir_path = os.path.abspath(os.getcwd())+'/download/'


file_data = dir_path+'/data.json'


chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : dir_path}
chromeOptions.add_experimental_option("prefs",prefs)
chromedriver = "chromedriver"

driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

# enable the debugger
# driver.execute_cdp_cmd("Debugger.enable", {})
# driver.execute_cdp_cmd("Debugger.setPauseOnExceptions", {"state": "all"})

# Open the main page
driver.get("https://apps.ute.com.uy/SgePublico/BajadasGE.aspx")    

data = file_get_contents(file_data) or {}
js_script_popup = """
// ---------------------------------------------------------------------
var div = document.createElement("div");
div.style.width = "300px";
div.style.height = "100px";
div.style.background = "red";
div.style.position = "absolute";
div.style.top = "0";
div.style.color = "white";
div.innerHTML = "Processing Data";
"""
driver.execute_script(js_script_popup)   

js_script = """

// ---------------------------------------------------------------------
var div = document.createElement("div");
div.style.width = "300px";
div.style.height = "100px";
div.style.background = "red";
div.style.position = "absolute";
div.style.top = "0";
div.style.color = "white";
div.innerHTML = "Processing Data";
// ---------------------------------------------------------------------
document.body.appendChild(div);
var _data =  {data};
if(typeof _data.cuencas != 'undefined'){{
    localStorage.setItem('data', JSON.stringify(_data));
    localStorage.setItem('System.init', true);
    localStorage.setItem('System.initSelenium', true);
}}
""".format(data=data) 
driver.execute_script(js_script)   



driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_optEmbalse").click()
time.sleep(2)

js_script = """
// ---------------------------------------------------------------------
document.mgrun = function(){
    var isSelenium = true;
    System.run(isSelenium);
}

var s = document.createElement("script"); 
s.src = "https://ml-as-a-service.com/tesis/extract_hierarchical_structure.js?v=1"; 
s.onload = function(e){ 
    console.log('Load ', s.src);
};  
document.head.appendChild(s);  
"""




for i in range(50):
    print('Process',i)
    driver.execute_script(js_script_popup) 
    driver.execute_script(js_script)   
    
    print('Init wait')
    time.sleep(np.random.randint(5,10)) 
    driver.execute_script(js_script_popup) 
    #WebDriverWait(driver,60).until(EC.visibility_of_element_located((By.ID,'mgInit')))
    try:
        print('Get Data')
        data = driver.execute_script('return JSON.parse(localStorage.getItem("data"))')
        print(data)
        file_put_contents(file_data, json.dumps(data))
    except:    
        print('')