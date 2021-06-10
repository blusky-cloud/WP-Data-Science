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
	print("WRITE CFDA (should be 1 per cfda)")
	print(csv_file)
	results = json_in['results']
	#print("RESULTS FROM WRITE METHOD pre insertion: ", results)
	if insert_list:
		for row in results:
			row['County FIPS Num'] = insert_list[0]
			row['County Name'] = insert_list[1]
	print("\n\n-------------------RESULTS FROM WRITE METHOD AFTER insertion: ", results)
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
	print("APPEND FILE: ", csv_file)
	results = json_in['results']
	print("\n\n append csv file results type and content: ", type(results), "\n", results)
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