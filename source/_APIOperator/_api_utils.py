import csv
import requests
import json
from requests_toolbelt.utils import dump


def read_column_from_file(file):
	num_list = []
	with open(file, 'r') as f:
		num_list = f.read().splitlines()
	f.close()
	return num_list


def read_csv(file):
	arr = []
	with open(file, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			arr.append(row)
	csvfile.close()
	return arr


def write_csv_list_to_file(lst, file):
	with open(file, 'w', newline='') as csvfile:
		# create the csv writer object
		csv_writer = csv.writer(csvfile)
		# Counter variable used for writing
		# headers to the CSV file
		for res in lst:
			csv_writer.writerow(res)
	csvfile.close()


def write_list_to_file(lst, file):
	with open(file, 'w', newline='') as f:
		for num in lst:
			f.write(num + '\n')
	f.close()


def write_new_cfda_csv_file(json_in, csv_file, insert_list=None):
	#print("WRITE CFDA (should be 1 per cfda)")
	#print(csv_file)
	results = json_in['results']
	#print("RESULTS FROM WRITE METHOD pre insertion: ", results)
	if insert_list:
		for row in results:
			row['County FIPS Num'] = insert_list[0]
			row['County Name'] = insert_list[1]
	#print("\n\n-------------------RESULTS FROM WRITE METHOD AFTER insertion: ", results)
	# now we will open a file for writing
	data_file = open(csv_file, 'w', newline='')
	# create the csv writer object
	csv_writer = csv.writer(data_file)
	# Counter variable used for writing
	# headers to the CSV file
	count = 0
	for res in results:
		if count == 0:
			# Writing headers of CSV file
			header = res.keys()
			try:
				csv_writer.writerow(header)
				csv_writer.writerow(res.values())
			except UnicodeEncodeError:
				print("count0 Write UnicodeEncodeError")
			count += 1
		else:
			# Writing data of CSV file
			try:
				csv_writer.writerow(res.values())
			except UnicodeEncodeError:
				print("Write UnicodeEncodeError")
				print("award ID: ", res['Award ID'])
				unicode_encode_award_ids(res['Award ID'])

	data_file.close()


def append_cfda_csv_file(json_in, csv_file, insert_list=None):
	#print("APPEND FILE: ", csv_file)
	results = json_in['results']
	#print("\n\n append csv file results type and content: ", type(results), "\n", results)
	if insert_list:
		for row in results:
			row['County FIPS Num'] = insert_list[0]
			row['County Name'] = insert_list[1]
	# now we will open a file for writing
	data_file = open(csv_file, 'a', newline='')
	# create the csv writer object
	csv_writer = csv.writer(data_file)
	# Counter variable used for writing
	# headers to the CSV file
	for res in results:
		csv_writer.writerow(res.values())
	data_file.close()

def unicode_encode_award_ids(id):
	with open('unicode_encode_error_award_ids.txt', 'a', newline='') as log:
		log.write(id)
		log.write("\n")
	log.close()


def append_sum_strs(qty, addend):
	#print(" APPEND ADDING, original: ", qty, ", addend: ", addend)
	fqty = round(float(qty), 6) # trial and error determined 6 places eliminated the long trailing decminal problems
	faddend = round(float(addend), 6)
	result = round((fqty + faddend), 3)
	#print("float converted qty: ", fqty, ", float convert addend: ", faddend, ", float result: ", result)
	#print("string result: ", str(result))
	return str(result)


def divide_strs(numerator, denominator):
	#  print(numerator, "/", denominator)
	n = round(float(numerator), 6)
	d = round(float(denominator.replace(',', '')))
	#  print("converted : ", n, "/", d)
	per_cap = round(n/d, 3)
	#  print("result (rounded) :", per_cap, ", as str: ", str(per_cap))
	return str(per_cap)


def tally_state_totals(cfda_csv_list, state_list):
	for row in cfda_csv_list:
		if row[17] == 'USA':  # index in sublist of country column
			for state in state_list:
				if state[2] == row[16]:  # state abbreviation from populations list, and state abbreviation column from cfda csv
					state[5] = append_sum_strs(state[5], row[5])  # because data is stored as strings
					state[9] = row[11]
	return state_list


def calculate_per_capita_spending(state_list):
	for state in state_list:
		state[7] = divide_strs(state[5], state[1])
	return state_list


def get_per_cap(s):
	return float(s[7])  # 5th column is per cap spending


def get_total_spending(s):
	return float(s[5])  # 4th column is total spending


def rank_states_per_cap_spending(state_list):
	state_list.sort(key=get_per_cap, reverse=True)
	# print("sorted: ", state_list)
	for s in state_list:
		s[8] = str(state_list.index(s) + 1)
	# print("state list: ", state_list)
	return state_list


def rank_states_total_spending(state_list):
	state_list.sort(key=get_total_spending, reverse=True)
	# print("sorted: ", state_list)
	for s in state_list:
		s[6] = str(state_list.index(s) + 1)
	# print("state list: ", state_list)
	return state_list
