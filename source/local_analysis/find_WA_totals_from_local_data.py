import pandas as pd
import csv
import requests
import bs4
import json
import time
from datetime import datetime
import zipfile
import pprint

data_root = "D:/Downloads/AwardDataArchiveAllAgenciesAllAssistance/"
yr_suffix = "_All_Assistance_Full_20210607/"
yr_prefix = "FY"
file_name_body = "_All_Assistance_Full_20210608_"

def set_path_yr(yr):
	return data_root + yr_prefix + str(yr) + yr_suffix


def set_csv_file(yr, num):
	return set_path_yr(yr) + yr_prefix + str(yr) + file_name_body + str(num) + '.csv'


def write_csv_list_to_file(lst, file):
	with open(file, 'w', newline='') as csvfile:
		# create the csv writer object
		csv_writer = csv.writer(csvfile)
		# Counter variable used for writing
		# headers to the CSV file
		for res in lst:
			csv_writer.writerow(res)
	csvfile.close()


# -------------------------------------------
#               DO STUFF
# -------------------------------------------
year = 2011
page = 1
current_file = set_csv_file(year, page)

data = pd.read_csv(current_file, low_memory=False)
print(data.head())
