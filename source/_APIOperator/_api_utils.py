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

