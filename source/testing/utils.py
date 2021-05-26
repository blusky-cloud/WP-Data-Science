import csv
import requests
import json
from requests_toolbelt.utils import dump
from time import sleep


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


def Ditch_Periods(file, new_file):
	print("ditch periods")
	arr = []
	with open(file, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			row[0] = row[0].replace('.', '')
			print(row)
			arr.append(row)
	csvfile.close()
	Write_CSVList(arr, new_file)
	return arr


def listify_csv(file):
	print("ditch periods")
	arr = []
	with open(file, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			#print(row)
			arr.append(row)
	csvfile.close()
	return arr


def read_abbreviations(file):
	print("add abbrev")
	arr = []
	with open(file, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			# print(row[2])
			arr.append(row[2])
	csvfile.close()
	return arr


def Write_CSVList(lst, file):
	with open(file, 'a', newline='') as csvfile:
		# create the csv writer object
		csv_writer = csv.writer(csvfile)
		# Counter variable used for writing
		# headers to the CSV file
		for res in lst:
			csv_writer.writerow(res)
	csvfile.close()


def StatePopReader(file):
	state_pops = {}
	with open(file, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			print(row['State'])
			state_pops.append(row['State'])
	csvfile.close()
	return state_pops


original_csv = listify_csv('2019_state_pops.csv')
abbrevs = read_abbreviations('csvData.csv')
print(original_csv)
#print(abbrevs)
ol = len(original_csv)
print(ol)
new_csv_list = original_csv
i = 0

for row in new_csv_list:
	row.append(abbrevs[new_csv_list.index(row)])


#for abbrev in abbrevs:
	#new_csv_list = [x + abbrev for x in new_csv_list]


print(new_csv_list)
Write_CSVList(new_csv_list, '2019_state_pops_wAbbrevs.csv')
#Ditch_Periods(state_pop_csv, '2019_est_state.csv')

