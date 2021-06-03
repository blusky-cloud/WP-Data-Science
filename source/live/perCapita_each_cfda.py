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


def append_sum_strs(qty, addend):
	#print(" APPEND ADDING, original: ", qty, ", addend: ", addend)
	fqty = round(float(qty), 6) # trial and error determined 6 places eliminated the long trailing decminal problems
	faddend = round(float(addend), 6)
	result = round((fqty + faddend), 3)
	#print("float converted qty: ", fqty, ", float convert addend: ", faddend, ", float result: ", result)
	#print("string result: ", str(result))
	return str(result)


def divide_strs(numerator, denominator):
	#print(numerator, "/", denominator)
	n = round(float(numerator), 6)
	d = round(float(denominator.replace(',', '')))
	#print("converted : ", n, "/", d)
	per_cap = round(n/d, 3)
	#print("result (rounded) :", per_cap, ", as str: ", str(per_cap))
	return str(per_cap)


def tally_state_totals(cfda_csv_list, state_list):
	for row in cfda_csv_list:
		if row[-4] == 'USA':
			# print("state: ", row[-5], " value: ", row[5])
			for state in state_list:
				if state[2] == row[-5]:
					state[4] = append_sum_strs(state[4], row[5])
	return state_list


def calculate_per_capita_spending(state_list):
	for state in state_list:
		state[5] = divide_strs(state[4], state[1])
	return state_list


def get_per_cap(state):
	return float(state[5])

def rank_states_per_cap_spending(state_list):
	list_to_check = []
	new_list = []
	compare = 0.00
	# list2 = sorted(state_list, key=get_per_cap)
	# print(list2)
	state_list.sort(key=get_per_cap, reverse=True)
	# print("sorted: ", state_list)
	for s in state_list:
		s[6] = str(state_list.index(s) + 1)
	# print("state list: ", state_list)
	return state_list


def Write_CSVList(lst, file):
	with open(file, 'w', newline='') as csvfile:
		# create the csv writer object
		csv_writer = csv.writer(csvfile)
		# Counter variable used for writing
		# headers to the CSV file
		for res in lst:
			csv_writer.writerow(res)
	csvfile.close()


# --------------------------------------------------------------------------------
#         STUFF HAPPENS NOW
# --------------------------------------------------------------------------------

cfda_index = 0
cfda_array = Read_CFDA_Nums_From_File(cfda_list_file)
#print(cfda_file_contents)
print("--------------------------------------------------")

#print(cfda_file_contents[1][-4])
#print(len(cfda_file_contents))

#if cfda_file_contents[1][-4] == 'USA':
	#print("USA id")
	#print(cfda_file_contents[1][-5])


index = 0
while index < len(cfda_array):
#while index < 1:
	print(cfda_array[index])
	cfda_file_contents = read_csv(set_CFDA_filename(cfda_array[index]))
	pops_list = read_csv(state_pops_file)
	per_cap_list = pops_list

	spent = '0.00'
	per_cap_spent = '0.00'
	rank = '0'

	per_cap_list[0].append('CFDA')
	per_cap_list[0].append('Total Spending')
	per_cap_list[0].append('Per Capita Spending')
	per_cap_list[0].append('Per Capita Rank')
	per_cap_data = per_cap_list[1::]

	for state in per_cap_data:
		state.append(cfda_array[index])
		state.append(spent)
		state.append(per_cap_spent)
		state.append(rank)

	per_cap_data = tally_state_totals(cfda_file_contents, per_cap_data)
	per_cap_data = calculate_per_capita_spending(per_cap_data)
	per_cap_data = rank_states_per_cap_spending(per_cap_data)

	final_list = per_cap_list[:1:] + per_cap_data

	Write_CSVList(final_list, set_state_CFDA_filename(cfda_array[index]))
	index += 1
print("--------------------------------------------------")