import csv
import requests
import json
from requests_toolbelt.utils import dump
from time import sleep

cfda_list_file = 'Updated_CFDA_list_noDuplicates.txt'
new_cfda_list_file = 'Updated_CFDA_list_noDuplicates.txt'
state_pop_csv = 'census2019statePopulationsDownloaded.csv'


def Read_CFDA_Nums_From_File(file):
	arr = []
	with open(file, 'r') as f:
		arr = f.read().splitlines()
	f.close()
	print(arr)
	return arr


def Eliminate_duplicate_CFDAs(arr):
	print(arr)
	new_arr = []
	for elem in arr:
		if elem not in new_arr:
			new_arr.append(elem)
	return new_arr


def Write_CFDA_list(file, list):
	with open(file, 'w', newline='') as outfile:
		for cfda in list:
			outfile.write(cfda)
			outfile.write('\n')


def StatePopReader(file):
	state_pops = {}
	with open(file, newline='') as csvfile:
		reader = csv.DictReader(csvfile)

	csvfile.close()
	return reader


pops = StatePopReader(state_pop_csv)

data = json.dumps(pops)
print(data)