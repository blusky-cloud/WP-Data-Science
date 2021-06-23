import pandas as pd
import csv
import requests
import bs4
import json
import time
from datetime import datetime
import zipfile
import pprint
import numpy as np
import dask.dataframe as dd
from glob import glob

data_root = "D:/Downloads/AwardDataArchiveAllAgenciesAllAssistance/"
yr_suffix = "_All_Assistance_Full_20210607/"
yr_prefix = "FY"
file_name_body = "_All_Assistance_Full_20210608_"
tnc_cfda_list_file = "../../data/reference/TNC_CFDA_list_formatted.txt"
state_pops_file = '2019_state_pops_wAbbrevs.csv'
cfda_abs_path = "C:/Users/whits/STUFF/WateryWater/Project/WP-Data-Science/data/reference/TNC_CFDA_list_formatted.txt"
pops_rel_path = "WP-Data-Science/source/local_analysis/2019_state_pops_wAbbrevs.csv"


def set_path_yr(yr):
	return data_root + yr_prefix + str(yr) + yr_suffix


def set_csv_file(yr, num):
	return set_path_yr(yr) + yr_prefix + str(yr) + file_name_body + str(num) + '.csv'


def set_glob_path_yr(yr):
	return set_path_yr(yr) + yr_prefix + str(yr) + file_name_body + '*.csv'

def write_csv_list_to_file(lst, file):
	print("writing file")
	with open(file, 'w', newline='') as csvfile:
		# create the csv writer object
		csv_writer = csv.writer(csvfile)
		# Counter variable used for writing
		# headers to the CSV file
		for res in lst:
			csv_writer.writerow(res)
	csvfile.close()


def read_column_from_file(file):
	num_list = []
	with open(file, 'r') as f:
		num_list = f.read().splitlines()
	f.close()
	for num in num_list:
		num = float(num)
	return num_list


def read_csv(file):
	arr = []
	with open(file, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			arr.append(row)
	csvfile.close()
	return arr


def pandas_testing():
	cfda_list = read_column_from_file(cfda_abs_path)
	state_pops = pd.read_csv(pops_rel_path)
	year = 2011
	page = 1
	current_file = set_csv_file(year, page)

	data = pd.read_csv(current_file, low_memory=False)

	# cfda_df = data.groupby('cfda_number')
	# tenninetwothree = cfda_df.get_group('10.923')
	# print(state_pops)
	# state_10923 = tenninetwothree.groupby('recipient_state_code')
	# state_10923.sum().reset_index().to_csv('state_10923_test1.csv')

	# new_file = set_csv_file(2011, 2)

	'''
	for i in range(2,6):
		new_file = set_csv_file(2011, i)
		temp_data = pd.read_csv(current_file, low_memory=False)
		data.append(temp_data)
	cfda_group = data.groupby('cfda_number')
	tenetc_all = cfda_group.get_group('10.923')
	state_10923_all = tenetc_all.groupby('recipient_state_code')
	state_10923.sum().reset_index().to_csv('state_10923_allpages_test3.csv')
	'''


def make_empty_totals_table():
	new_table = [['CFDA NUM', 'CFDA Name', 'Sub-Tier', 'WP Category', 'Types of Assistance'], ['10.001']]

	cfda_list = read_column_from_file(cfda_abs_path)
	pops_list = read_csv(state_pops_file)

	for cfda in cfda_list[1::]:
		new_num = []
		new_num.append(str(cfda))
		new_table.append(new_num)
	for state in pops_list[1::]:
		new_table[0].append(state[2] + ' total obligated amount')
		new_table[0].append(state[2] + ' total non federal funding amount')
		new_table[0].append(state[2] + ' total funding amount')
		new_table[0].append(state[2] + ' total face value of loan')
	new_table[0].append('Other total obligated amount')
	new_table[0].append('Other total non federal funding amount')
	new_table[0].append('Other  total funding amount')
	new_table[0].append('Other  total face value of loan')
	for row in new_table[1::]:
		for i in range(4):
			row.append('NA')
		for state in pops_list[1::]:
			row.append('0.00')
			row.append('0.00')
			row.append('0.00')
			row.append('0.00')
		row.append('0.00')
		row.append('0.00')
		row.append('0.00')
		row.append('0.00')

	print(new_table)
	write_csv_list_to_file(new_table, 'new_table_empty2.csv')


def append_sum_strs(qty, addend, verbose=True):
	if verbose:
		print("                                 appending sum strs")
		print("                                 0APPEND ADDING, original: ", qty, ", addend: ", addend, type(qty), " ",
			  type(addend))

	try:
		fqty = round(float(qty), 6)  # trial and error determined 6 places eliminated the long trailing decminal problem
	except ValueError as v:
		print(v)
		print("val error sumstrs, original qty: ", qty)
		fqty = 0.00

	try:
		faddend = round(float(addend), 6)
	except ValueError as v:
		print(v)
		print("val error sumstrs, original addend: ", qty)
		faddend = 0.00

	result = round((fqty + faddend), 3)

	if qty != '0.00' and qty != '0.0' and verbose:
		print(" 1APPEND ADDING, original: ", qty, ", addend: ", addend, type(qty), " ", type(addend))
		print("float converted qty: ", fqty, ", float convert addend: ", faddend, ", float result: ", result)
	elif addend != '0.00' and addend != '0.0' and addend != '' and verbose:
		print(" 2APPEND ADDING, original: ", qty, ", addend: ", addend, " types are: ", type(qty), " ", type(addend))
		print("float converted qty: ", fqty, ", float convert addend: ", faddend, ", float result: ", result)
	if verbose:
		print("       append string result: ", str(result))
	return str(result)


def divide_strs(numerator, denominator):
	#  print(numerator, "/", denominator)
	n = round(float(numerator), 6)
	d = round(float(denominator.replace(',', '')))
	#  print("converted : ", n, "/", d)
	per_cap = round(n / d, 3)
	#  print("result (rounded) :", per_cap, ", as str: ", str(per_cap))
	return str(per_cap)


def tally_state_totals(cfda_csv_list, state_list):
	for row in cfda_csv_list:
		if row[17] == 'USA':  # index in sublist of country column
			for state in state_list:
				if state[2] == row[
					16]:  # state abbreviation from populations list, and state abbreviation column from cfda csv
					state[5] = append_sum_strs(state[5], row[5])  # because data is stored as strings
					state[9] = row[11]
	return state_list


def get_base_index_for_state(state, save_list):
	for entry in save_list[0]:
		if entry[:2:] == state:
			# print(entry[:2:])
			return int(save_list[0].index(entry))


def process_row_match(save_list, row, cfda, yr_table, verbose=True):
	# print("match cfda: ", cfda, " state: ", row[49])
	base_index = get_base_index_for_state(row[49], save_list)
	# print(base_index, "type: ", type(base_index))
	pre_value = 0.00
	real_error = False
	if base_index is None:
		# print("overriding type")
		base_index = 209
	for (num, yr_num) in zip(save_list[1::], yr_table[1::]):
		if float(num[0]) == float(cfda):
			for i in range(4):
				if num[base_index + i] != '0.00' and num[base_index + i] != '0.0' and verbose:
					print("i is: ", i, " ORIGINAL TABLE VAL: ", num[base_index + i], " cfda: ", cfda,
						  " save table index: ", base_index + i, " ADDEND: ", row[7 + i])
					print("row: ", row)
					print("row index: ", row[7 + i])

				pre_value = float(num[base_index + i])

				if row[7 + i] != '0.00' and row[7 + i] != '0.0' and verbose:
					print("row index value from process row match: ", row[7 + i])

				if row[7 + i] != '0.00' and row[7 + i] != '0.0' and row[7 + i] != '':
					yr_num[base_index + i] = num[base_index + i] = append_sum_strs(num[base_index + i], row[7 + i],
																				   verbose)

				if row[7 + i] != '0.00' and row[7 + i] != '0.0' and row[7 + i] != '' and verbose:
					if float(num[base_index + i]) == pre_value:
						real_error = True
						return save_list, yr_table, real_error

				if num[base_index + i] != '0.00' and num[base_index + i] != '0.0' and verbose:
					print("i is: ", i, " NEW TABLE VAL  ------  : ", num[base_index + i], " cfda: ", cfda,
						  " save table index: ", base_index + i)

	'''for num in yr_table[1::]:
		if float(num[0]) == float(cfda):
			for i in range(4):
				num[base_index + i] = append_sum_strs(num[base_index + i], row[7 + i])'''
	return save_list, yr_table, real_error


def check_exceptions(new_table, year, page, yr_table, verbose=True):
	print("Check Exceptions")
	str_cfda_list = read_column_from_file(cfda_abs_path)
	cfda_list = []
	err_case = False
	for n in str_cfda_list:
		cfda_list.append(float(n))
	# print("cfda list elem type: ", type(cfda_list[1]), " ", cfda_list[1])
	pops_list = read_csv(state_pops_file)
	current_file = set_csv_file(year, page)
	# print(cfda_list, pops_list, current_file)
	count_count = 0
	prev_count = 0
	file_not_finished = True
	with open(current_file, 'r', newline='') as file:
		dialect = csv.Sniffer().sniff(file.read(1024))
		file.seek(0)
		datareader = csv.reader(file, strict=True, dialect='excel')
		count = 0
		while file_not_finished:
			try:
				for row in datareader:
					# print(count)
					if count % 50000 == 0:
						print("year: ", year, " page: ", page, " count: ", count)
					# print(row[68], "and now for the amount: ", row[7])
					try:
						# print("type of index 68: ", type(row[68]))
						if count and float(row[68]) in cfda_list:
							# print("cfda match: ", row[68], "  yeay!", row)
							new_table, yr_table, err_case = process_row_match(new_table, row, row[68], yr_table,
																			  verbose)
							if err_case:
								print("ERROR CASE, row: ", row)
								return new_table, yr_table, err_case
							if row[7] != '0.00' and row[7] != '0.0' and row[7] != '' and verbose:
								print("row[7] is: ", row[7], " line is: ", datareader.line_num)

					except UnicodeDecodeError:
						print("unicode decode error!")
						# print(row)
						pass
					except ValueError as v:
						print(v)
						print("Value error output, cfda: ", row[68])
						print(row[68])
						print("len row: ", len(row), "row: ", row)
						datareader.__next__()
						# print("log this maybe?")
						pass
					except IndexError:
						# print('index error, count is: ', count, " year: ", year, " page: ", page)
						pass
					count += 1
			except UnicodeDecodeError:
				# print("big whoops")
				# print(row)
				pass
			if count == prev_count:
				count_count += 1
				if count_count > 2:
					file_not_finished = False

			prev_count = count

	print("done with page")
	return new_table, yr_table, error_state


def process_pd_chunk(chunk, output_file, table, cfda_l):
	print("process chunk")
	chunk = chunk.fillna("UNSPECIFIED")

	tnc = chunk.loc[chunk['cfda_number'].isin(cfda_l)]
	#tnc_states = tnc.groupby(['cfda_number', 'recipient_state_code'])
	#print(tnc_states.groups, tnc_states.indices)
	#print(tnc_states.head())
	#tnc_states.to_csv('test_2011_1_groups_full.csv')
	#tnc_states.sum().reset_index().to_csv('states_chunktest2.csv')
	# cfda_df = chunk.groupby('cfda_number')
	# tenninetwothree = cfda_df.get_group('10.923')
	# print(state_pops)
	# state_10923 = tenninetwothree.groupby('recipient_state_code')
	# state_10923.sum().reset_index().to_csv('state_10923_test1.csv')
	return tnc


def pandas_bites(yr, pg, output_file, table_file):
	print("pandas bites")
	str_cfda_list = read_column_from_file(cfda_abs_path)
	cfda_list = []
	for n in str_cfda_list:
		cfda_list.append(float(n))
	pops_list = read_csv(state_pops_file)
	table = read_csv(table_file)

	curr_file = set_csv_file(yr, pg)

	print("now to take a bite, pg: ", pg)
	rel_columns = [7, 8, 9, 10, 49, 68]
	col_types = {
		'total_obligated_amount': convert_num_from_str,
		'non_federal_funding_amount': convert_num_from_str,
		'total_non_federal_funding_amount': convert_num_from_str,
		'face_value_of_loan': convert_num_from_str,
		'cfda_number': convert_num_from_str,
		'recipient_state_code': str
	}
	chunksize = 100000
	chunk_results = pd.DataFrame
	acc_temp_results = pd.DataFrame
	accumulated_results = pd.DataFrame
	full_frame = pd.DataFrame
	count = 0
	with pd.read_csv(curr_file, usecols=rel_columns, converters=col_types, chunksize=chunksize) as reader:
		for chunk in reader:
			print("iter")
			chunk_results = process_pd_chunk(chunk, output_file, table, cfda_list)
			if not count:
				print("not count")
				acc_temp_results = accumulated_results = chunk_results
				#print(accumulated_results.info, accumulated_results.columns)
				count += 1
			else:
				#print("first: ", accumulated_results.info)
				#print("adding: ", chunk_results.info)
				accumulated_results = chunk_results.combine(accumulated_results, combine_chunks, fill_value=0)
				#print("second: ", accumulated_results.info)
				acc_temp_results = accumulated_results
				count += 1
	#tnc_states = accumulated_results.groupby(['cfda_number', 'recipient_state_code'])
	#tnc_states.sum().reset_index().to_csv('states_allchunktest3.csv')
	return accumulated_results

def convert_num_from_str(val):
	cfda = 0.00
	try:
		cfda = np.float64(val)
		return cfda
	except ValueError:
		cfda = 0.00
		return cfda


def combine_chunks(s1, s2):
	#print("s1 type: ", s1.dtype, " s2 type: ", s2.dtype)
	#print("s1: ", s1)
	#print("s2: ", s2)
	if s1.name == 'cfda_number' or s1.name == 'recipient_state_code':
		return s1
	if s1.dtype == object or s2.dtype == object:
		return s1
	elif s1.name == s2.name:
		return s1.combine(s2, add_series_vals, fill_value=0)


def add_series_vals(first, second):
	#print("add first: ", first, "add second: ", second, " types: ", type(first), type(second))
	if first != 0 and second != 0:
		print("add first: ", first, "add second: ", second, " types: ", type(first), type(second))
		return first + second


def try_dask(yr, pg, cfda_l):
	print("try dask")
	curr_file = set_glob_path_yr(yr)
	print(curr_file)
	rel_columns = [7, 8, 9, 10, 49, 68]
	col_types = {
		'total_obligated_amount': convert_num_from_str,
		'non_federal_funding_amount': convert_num_from_str,
		'total_non_federal_funding_amount': convert_num_from_str,
		'face_value_of_loan': convert_num_from_str,
		'cfda_number': convert_num_from_str,
		'recipient_state_code': str
	}
#quoting=csv.QUOTE_NONE, error_bad_lines=False, engine='python'
	#the above args to read_csv prevented an EOF error but slowed things wayyy down
	df = dd.read_csv(curr_file, usecols=rel_columns, converters=col_types, engine='python', error_bad_lines=False)
	tnc = df.loc[df['cfda_number'].isin(cfda_l)]
	#tnc_states = tnc.groupby(['cfda_number', 'recipient_state_code'])
	#tnc_states.sum().reset_index().to_csv(str(yr) + '_dask2.csv', single_file=True)
	tnc.to_csv(str(yr) + '_noSum1_dask.csv', single_file=True)


def try_dask_allglob(cfda_l):
	print("try dask")
	gl_pth = 'D:/Downloads/AwardDataArchiveAllAgenciesAllAssistance/FY*_All_Assistance_Full_20210607/FY*_All_Assistance_Full_20210608_*.csv'
	curr_file = gl_pth
	print(curr_file)
	rel_columns = [7, 8, 9, 10, 49, 68]
	col_types = {
		'total_obligated_amount': convert_num_from_str,
		'non_federal_funding_amount': convert_num_from_str,
		'total_non_federal_funding_amount': convert_num_from_str,
		'face_value_of_loan': convert_num_from_str,
		'cfda_number': convert_num_from_str,
		'recipient_state_code': str
	}
#quoting=csv.QUOTE_NONE, error_bad_lines=False, engine='python'
	#the above args to read_csv prevented an EOF error but slowed things wayyy down
	df = dd.read_csv(curr_file, usecols=rel_columns, converters=col_types, engine='python', error_bad_lines=False)
	tnc = df.loc[df['cfda_number'].isin(cfda_l)]
	#tnc_states = tnc.groupby(['cfda_number', 'recipient_state_code'])
	#tnc_states.sum().reset_index().to_csv('Allyrs_dask2.csv', single_file=True)
	tnc.to_csv('all_years_noSum1_dask2.csv', single_file=True)

# -------------------------------------------
#               DO STUFF
# -------------------------------------------
# make_empty_totals_table()
print(" Commencing Data Analysis Operations")
output_file = 'attempt_count_totals2.csv'
pandas_save_file = 'pandas_2011_attempt1.csv'
empty_table_file = 'new_table_empty2.csv'
error_state = False
year = 2011
page = 1
new_table = read_csv('new_table_empty2.csv')
yr_table = read_csv('new_table_empty2.csv')
write_csv_list_to_file(new_table, output_file)

year_not_done = True
df = pd.DataFrame
str_cfda_list = read_column_from_file(cfda_abs_path)
cfda_list = []
for n in str_cfda_list:
	cfda_list.append(float(n))
years = [2018, 2020, 2021]

for year in range(2011, 2022):
	try_dask(year, page, cfda_list)

try_dask_allglob(cfda_list)

'''for page in range(5):
	if page == 0:
		df = pandas_bites(year, page+1, pandas_save_file, empty_table_file)
	else:
		df = pandas_bites(year, page+1, pandas_save_file, empty_table_file).combine(df, combine_chunks, fill_value=0)

tnc_states = df.groupby(['cfda_number', 'recipient_state_code'])
tnc_states.sum().reset_index().to_csv('2011_bychunks_test1.csv')



while year < 2022:
	page = 1
	year_not_done = True
	try:
		while year_not_done:
			new_table = read_csv(output_file)
			try:
				print("year: ", year, " page: ", page)
				new_table, yr_table, error_state = check_exceptions(new_table, year, page, yr_table, verbose=False)
				if error_state:
					print("back in main, ERROR STATE")
					break
				write_csv_list_to_file(new_table, output_file)
				if page == 5:
					print("done")
					break
				page += 1
			except FileNotFoundError:
				print("page file not found")
				year_not_done = False
				year += 1
				break

	except FileNotFoundError:
		print("year file not found")
		pass
	if year == 2011 and page == 5:
		write_csv_list_to_file(yr_table, 'year_attempt2_count_totals_FY' + str(year - 1) + '.csv')
		break
	if error_state:
		break

	write_csv_list_to_file(yr_table, 'year_attempt2_count_totals_FY' + str(year - 1) + '.csv')
	yr_table = read_csv('new_table_empty2.csv')
	'''
