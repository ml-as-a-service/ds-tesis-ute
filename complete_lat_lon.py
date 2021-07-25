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
file_data_latlon = dir_path+'/MapaEstHid.aspx'
file_data_latlon_raw_csv = dir_path+'/MapaEstHid.csv'
file_data_fullpath_csv = dir_path+'/data_fullpath.csv'
file_data_fullpath_without_paso_csv = dir_path+'/data_fullpath_without_paso.csv'

file_data_merged_latlon_path_csv = dir_path+'/data_merged_latlon_path.csv'
file_data_merged_path_latlon_csv = dir_path+'/data_merged_path_latlon.csv'

file_data_latlon_csv = dir_path+'/data_latlon.csv'

import pandas as pd  
df = pd.read_csv(file_data_fullpath_csv)
# estado,cuenca,subcuenca,estacion,paso
df.drop(['estado','paso'], inplace=True, axis=1)
df.drop_duplicates(subset=None, inplace=True)
df.to_csv(file_data_fullpath_without_paso_csv, index=False)


# -------------------------------------------------------------------------
# estado,cuenca,subcuenca,estacion,paso
df_path = pd.read_csv(file_data_fullpath_without_paso_csv)

df_path['cuenca_id'] = df_path['cuenca'].str.extract(r"(\w+)")  
df_path['cuenca_name'] = df_path['cuenca'].str.extract(r"(\([\w\s.-]+\))")

df_path['subcuenca_id'] = df_path['subcuenca'].str.extract(r"(\w+)")  
df_path['subcuenca_name'] = df_path['subcuenca'].str.extract(r"(\([\w\s.-]+\))")

df_path['estacion_id'] = df_path['estacion'].str.extract(r"(\w+)")  
df_path['estacion_name'] = df_path['estacion'].str.extract(r"(\([\w\s.-]+\))")

df_path.drop(['cuenca','subcuenca','estacion'], inplace=True, axis=1)

# df_path.to_csv(file_data_borrar_csv, index=False)


# -------------------------------------------------------------------------
# "id","name","lat","lon","type"
df_latlon = pd.read_csv(file_data_latlon_raw_csv)
df_latlon['estacion_name'] = '('+df_latlon['name'].str.strip()+')'
# df_latlon.to_csv(file_data_borrar_csv, index=False)



# # Join by id_estacion
# df_latlon_path = df_latlon.set_index('id_estacion').join(df_path.set_index('id_estacion'))
# df_latlon_path.to_csv(file_data_merged_latlon_path_csv, index=False)

# Join by id_estacion
df_path_latlon = df_path.join(df_latlon.set_index('estacion_name'), on="estacion_name")
 
df_path_latlon['cuenca_name'] = df_path_latlon['cuenca_name'].str[1:-1]
df_path_latlon['subcuenca_name'] = df_path_latlon['subcuenca_name'].str[1:-1]
df_path_latlon['estacion_name'] = df_path_latlon['estacion_name'].str[1:-1]

df_path_latlon.drop(['id','name' ], inplace=True, axis=1)
df_path_latlon.to_csv(file_data_latlon_csv, index=False)
