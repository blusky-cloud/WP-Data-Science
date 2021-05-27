import csv
import requests
import json
from requests_toolbelt.utils import dump
from time import sleep

cfda_list_file = 'Updated_CFDA_list_noDuplicates.txt'
state_pops_file = '2019_state_pops_wAbbrevs.csv'
output_file_path = '../../data/analysis/state_breakdown_per_cfda/'
data_file_path = '../../data/individual_csv_files_per_cfda/'
csv_file_name = 'CFDA_'
state_csv_file_name = 'state_CFDA_'
curr_cfda_file = data_file_path + csv_file_name


def set_CFDA_filename(cfda):
	cfda_file = data_file_path + csv_file_name + str(cfda).replace('.', '') + '.csv'
	return cfda_file


def set_state_CFDA_filename(cfda):
	state_cfda_file = output_file_path + state_csv_file_name + str(cfda).replace('.', '') + '.csv'
	return state_cfda_file


def Read_CFDA_Nums_From_File(file):
	arr = []
	with open(file, 'r') as f:
		arr = f.read().splitlines()
	f.close()
	# print(arr)
	return arr


def read_csv(file):
	arr = []
	with open(file, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			arr.append(row)
	csvfile.close()
	return arr

cfda_index = 0
cfda_array = Read_CFDA_Nums_From_File(cfda_list_file)
cfda_file_contents = read_csv(set_CFDA_filename(cfda_array[cfda_index]))
#print(cfda_file_contents)
print("--------------------------------------------------")

#print(cfda_file_contents[1][-4])
#print(len(cfda_file_contents))

#if cfda_file_contents[1][-4] == 'USA':
	#print("USA id")
	#print(cfda_file_contents[1][-5])

pops_list = read_csv(state_pops_file)
per_cap_list = pops_list

spent = '0.00'
per_cap_spent = '0.00'

per_cap_list[0].append('CFDA')
per_cap_list[0].append('Total Spending')
per_cap_list[0].append('Per Capita Spending')

for state in per_cap_list[1::]:
	state.append(cfda_array[cfda_index])
	state.append(spent)
	state.append(per_cap_spent)
print(per_cap_list)



