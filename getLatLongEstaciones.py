import requests
from bs4 import BeautifulSoup

import os
import json
import mylib
import pandas as pd
from shutil import copyfile
import csv 
 
# Download Dir
dir_path = os.path.abspath(os.getcwd())+'/download/'
dir_path_ute = dir_path+'ute/'
file_data_latlon = dir_path+'/MapaEstHid.aspx'
file_data_latlon_csv = dir_path+'/MapaEstHid.csv'

# download data
if not os.path.isfile(file_data_latlon) :
    print("### downloading file ", file_data_latlon)
    # url = "https://apps.ute.com.uy/SgePublico/MapaEstacionesHid.aspx"
    url = "https://apps.ute.com.uy/SgePublico/MapaEstHid.aspx"

    r = requests.get(url)  
    mylib.file_put_contents(file_data_latlon, r.content)

html = mylib.file_get_contents(file_data_latlon)

# Scrapping
soup = BeautifulSoup(html, "html.parser")
results = soup.findAll("li", {"data-gmapping" : True})

mapping = [['id','name','lat','lon','type']]
for result in results :
    data_gmapping = json.loads(result["data-gmapping"])
    # print(data_gmapping)
    mapping.append([
        data_gmapping['id'],
        data_gmapping['text'],
        data_gmapping['latlng']['lat'],
        data_gmapping['latlng']['lng'],
        data_gmapping['tipo']
    ])

print(mapping)
with open(file_data_latlon_csv, 'w', newline='') as file:
    mywriter = csv.writer(file, delimiter=',', quoting=csv.QUOTE_ALL)
    mywriter.writerows(mapping)