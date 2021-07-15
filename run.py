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
import glob
import mylib
import pandas as pd
from shutil import copyfile
 
# Download Dir
dir_path = os.path.abspath(os.getcwd())+'/download/'
dir_path_ute = dir_path+'ute/'
dir_path_ute_data = dir_path_ute+'data/'
file_data_csv = dir_path+'/data.csv'

# file_script = os.path.abspath(os.getcwd())+'/parse_html/dist/extract_hierarchical_structure.js';
# content_script = mylib.file_get_contents(file_script)
content_script = """
document.mgrun = function(){
    //System.run();
}

var s = document.createElement("script"); 
s.src = "https://ml-as-a-service.com/tesis/extract_hierarchical_structure.js?v=1"; 
s.onload = function(e){ 
    console.log('Load ', s.src);
};  
document.head.appendChild(s);  
"""

driver = None 

def getDriver(year):
    dir_download = dir_path+'/ute/'+str(year)+'/'
    # os.rmdir(dir_download)
    os.mkdir(dir_download)

    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : dir_download}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = "chromedriver"

    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

    # Open the main page
    driver.get("https://apps.ute.com.uy/SgePublico/BajadasGE.aspx")    

    # for cache
    driver.execute_script(content_script) 

    driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_optEmbalse").click()
    time.sleep(2)
    return driver
    
  
df = pd.read_csv(file_data_csv) 

driver = getDriver('20210714')
# months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Setiembre","Octubre","Noviembre","Diciembre"]
months = ["Enero","Junio","Diciembre"]
years = [*range(2000,2021)]

# def showFileCount():
#     dir = dir_path+'/ute/20210714/'
#     print('-->showFileCount',dir, len([name for name in os.listdir(dir)]))

def showLastFileCreated():
    dir = dir_path+'/ute/20210714/'
    list_of_files = glob.glob(dir+'*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)   
    return latest_file 


count_download = 0

for iy, y in enumerate(years):
    print('------ Init Year -------------------------------------------------', y)
    for im, m in enumerate(months):
        if (im == len(months)-1): 
            continue
        print('------ Init Month -------------------------------------------------', m)
        timeParams = {
            "driver": driver,
            "cboAnioIni": y,
            "cboMesIni": m,
            "cboAnioFin": y,
            "cboMesFin": months[im+1]
        }
        mylib.setTimeFilter(timeParams);

        for index, row in df.iterrows():
            dst = dir_path_ute_data+"/{}-{}-{}-{}-{}-{}-{}-{}.txt".format(
                y,m,y,months[im+1],
                row["cuenca"],row["subcuenca"],row["estacion"],row["paso"]
            )
            if os.path.exists(dst):
                print('Proccesed', dst)
                continue


            cuencaParameters = {
                "driver": driver,
                "cuenca": row["cuenca"],
                "subcuenca": row["subcuenca"],
                "estacion": row["estacion"],
                "paso": row["paso"],                
            }
            mylib.setCuencaFilter(cuencaParameters)
            
            driver.execute_script(content_script)   
            time.sleep(2)

            print("\n\n------ download -------------------------------------------------\n")
            print(timeParams)
            print(cuencaParameters)
            print(driver.execute_script('return System.getSelectedOptions();'))

            mylib.download(driver)
            src = showLastFileCreated()
            copyfile(src, dst)





# driver.quit()
