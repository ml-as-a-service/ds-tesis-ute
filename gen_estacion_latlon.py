import os
import json
import mylib
import pandas as pd
from shutil import copyfile
import csv 
from csv import DictReader
 
# Download Dir
dir_path = os.path.abspath(os.getcwd())+'/download/'
dir_path_ute = dir_path+'ute/' 
dir_path_ute_data = dir_path_ute+'data/'
dir_path_ute_csv = dir_path_ute+'csv/'

import glob
import ntpath
# ntpath.basename("a/b/c")

for f in glob.glob(dir_path_ute_data+'*'):
    file_name_out = dir_path_ute_csv+ntpath.basename(f).replace('.txt','.csv')
    mylib.gen_estacion_latlon(f, file_name_out)
    
    # print(f, ntpath.basename(f))