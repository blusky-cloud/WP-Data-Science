import csv
import requests
import json
from requests_toolbelt.utils import dump
from _api_utils import read_column_from_file, write_csv_list_to_file, write_list_to_file, read_csv, \
	write_new_cfda_csv_file, append_cfda_csv_file


class APIOperator(object):
	url_root = 'https://api.usaspending.gov'
	api = {
		'spending_by_award': '/api/v2/search/spending_by_award/',
		'all_cfda_totals': '/api/v2/references/cfda/totals/',
		'spending_by_category_cfda': "/api/v2/search/spending_by_category/cfda/"
	}
	body = {
		"filters": {
			"time_period": [
				{"start_date": "2012-10-01", "end_date": "2013-09-30"},
				{"start_date": "2013-10-01", "end_date": "2014-09-30"},
				{"start_date": "2014-10-01", "end_date": "2015-09-30"},
				{"start_date": "2015-10-01", "end_date": "2016-09-30"},
				{"start_date": "2016-10-01", "end_date": "2017-09-30"},
				{"start_date": "2017-10-01", "end_date": "2018-09-30"},
				{"start_date": "2007-10-01", "end_date": "2008-09-30"},
				{"start_date": "2018-10-01", "end_date": "2019-09-30"},
				{"start_date": "2008-10-01", "end_date": "2009-09-30"},
				{"start_date": "2019-10-01", "end_date": "2020-09-30"},
				{"start_date": "2009-10-01", "end_date": "2010-09-30"},
				{"start_date": "2020-10-01", "end_date": "2021-09-30"},
				{"start_date": "2010-10-01", "end_date": "2011-09-30"},
				{"start_date": "2011-10-01", "end_date": "2012-09-30"}
			],
			"award_type_codes": [
				"02", "03", "04", "05"
			],
			"place_of_performance_locations": [
				{
					"country": "USA",
					"state": "WA",
					"county": "001"
				}
			],
			"program_numbers": [
				"10.001"
			]
		},
		"fields": [
			"Award ID", "Recipient Name", "Start Date", "End Date", "Award Amount", "Description", "def_codes",
			"Awarding Agency", "Awarding Sub Agency", "Award Type",
			"recipient_id", "prime_award_recipient_id", "CFDA Number", "Place of Performance State Code",
			"Place of Performance Country Code", "Place of Performance Zip5", "Place of Performance City Code",
			"Funding Agency Code", "Recipient DUNS Number", "Awarding Agency Code",
			"Start Date", "End Date", "SAI Number", "Base Obligation Date", "generated_internal_id",
			"Issued Date", "Last Modified Date"
		],
		"page": 1,
		"limit": 100,
		"sort": "Award Amount",
		"order": "desc",
		"subawards": False
	}
	cfda_num_list = []

	def __init__(
			self,
			b=None,
			cfda_list_file='',
			reference_root_path='../../data/reference/',
			county_ref_info_path='../../data/reference/WA FIPS + 2019 pop estimates - Sheet1.csv'):
		print(" initiating APIOperator ")
		if b is not None:
			self.body = b
		if cfda_list_file != '':
			self.cfda_num_list = self.read_cfda_list_from_file(cfda_list_file)
		self.downloading = True
		self.page_to_request = 1
		self.is_first_contact = True
		self.curr_cfda_list_index = 0
		self.response_from_server = requests.models.Response()
		self.server_resp_json = {}
		self.server_resp_json_obj = {}
		self.cfda_and_name_list = []
		self.ref_root_path = reference_root_path
		self.cfda_file_name = ''
		self.wa_county_names = read_csv(county_ref_info_path)

	def __str(self):
		print("BODY: ", self.body)

	def make_url(self, endpoint):
		return self.url_root + self.api[endpoint]

	def set_state_cfda_filename(self, cfda):
		state_cfda_file = '../../data/analysis/state_breakdown_per_TNC_cfda/state_CFDA_' + str(cfda).replace('.',
																											 '') + '.csv'
		return state_cfda_file

	def set_cfda_filename(self, cfda, path='../../data/TNC_CFDA_list/WA_Counties/CFDA_'):
		self.cfda_file_name = path + str(cfda).replace('.', '') + '.csv'
		return self.cfda_file_name

	def read_cfda_list_from_file(self, file):
		with open(file, 'r') as f:
			self.cfda_num_list = f.read().splitlines()
		f.close()
		return self.cfda_num_list

	def update_request_body_cfda(self, cfda, b=None):
		if b is not None:
			b['filters']['program_numbers'][0] = cfda
			return b
		else:
			self.body['filters']['program_numbers'][0] = cfda
			return self.body

	def update_request_body_county(self, county_code, b=None):
		if b is not None:
			b['filters']['place_of_performance_locations'][0]['county'] = county_code
			return b
		else:
			self.body['filters']['place_of_performance_locations'][0]['county'] = county_code
			return self.body

	def post_request(self, endpoint):
		headers = {'Content-Type': 'application/json'}
		payload = self.body
		self.response_from_server = requests.post(self.make_url(endpoint), headers=headers, json=payload)
		return self.response_from_server

	def post_req_newpage(self, url, page):
		headers = {'Content-Type': 'application/json'}
		self.body['page'] = page
		payload = self.body
		self.response_from_server = requests.post(url, headers=headers, json=payload)
		return self.response_from_server

	def jsonify(self):
		# This line extracts the JSON data out of the message we got from the server
		self.server_resp_json = self.response_from_server.json()
		# This encodes it as a bytestream
		res_bytes = json.dumps(self.server_resp_json).encode('utf-8')
		# This loads the bytestream into a json_object
		self.server_resp_json_obj = json.loads(res_bytes)
		return self.server_resp_json

	def pretty_print_server_response(self):
		print("NOW PRINTING ENTIRE RESPONSE")
		data = dump.dump_all(self.response_from_server)
		print(data.decode('utf-8'))

	def pretty_print_server_data(self, s=None):
		if s is not None:
			json_from_server = s.json()
			res_bytes = json.dumps(json_from_server).encode('utf-8')
			# This loads the bytestream into a json_object
			json_object = json.loads(res_bytes)
			# This converts the json_object to a form that can be printed to the terminal (string)
			json_formatted_str = json.dumps(json_object, indent=2)
			# Print the nicely formatted json data to the terminal
			print("NOW PRINTING NICELY FORMATTED JSON WE RECEIVED FROM THE SERVER:")
			print(json_formatted_str)
		else:
			json_from_server = self.response_from_server.json()
			res_bytes = json.dumps(json_from_server).encode('utf-8')
			# This loads the bytestream into a json_object
			json_object = json.loads(res_bytes)
			# This converts the json_object to a form that can be printed to the terminal (string)
			json_formatted_str = json.dumps(json_object, indent=2)
			# Print the nicely formatted json data to the terminal
			print("NOW PRINTING NICELY FORMATTED JSON WE RECEIVED FROM THE SERVER:")
			print(json_formatted_str)

	def pretty_print_json(self, j={}, body=False):
		if not body and j:
			res_bytes = json.dumps(j).encode('utf-8')
			# This loads the bytestream into a json_object
			json_object = json.loads(res_bytes)
			# This converts the json_object to a form that can be printed to the terminal (string)
			json_formatted_str = json.dumps(json_object, indent=2)
			# Print the nicely formatted json data to the terminal
			print("NOW PRINTING NICELY FORMATTED JSON ")
			print(json_formatted_str)
		elif body:
			res_bytes = json.dumps(self.body).encode('utf-8')
			# This loads the bytestream into a json_object
			json_object = json.loads(res_bytes)
			# This converts the json_object to a form that can be printed to the terminal (string)
			json_formatted_str = json.dumps(json_object, indent=2)
			# Print the nicely formatted json data to the terminal
			print("NOW PRINTING NICELY FORMATTED JSON ")
			print(json_formatted_str)

	def test_request(self):
		self.post_request('all_cfda_totals')
		self.pretty_print_server_response()

	# method for a POST taking endpoint whose response includes the names for the cfda nums searched
	def spending_by_category_cfda(self, body={}, display=True):
		# print("spending by cat: cfda")
		headers = {'Content-Type': 'application/json'}
		payload = body
		# print(f"body: {body}")
		api_name = "spending_by_category_cfda"
		url_api = self.make_url(api_name)
		# print(f"url_api: {url_api}")
		r = requests.post(url_api, headers=headers, json=payload)
		self.response_from_server = r
		if display:
			# print("spend by cat cfda display")
			self.pretty_print_server_data()
		return r

	# useless
	def all_cfda_totals(self, display=True):
		print("all cfda totals")
		headers = {'Content-Type': 'application/json'}
		api_name = 'all_cfda_totals'
		url_api = self.make_url(api_name)
		print(f"url_api: {url_api}")
		r = requests.get(url_api)
		if display:
			json_from_server = r.json()
			res_bytes = json.dumps(json_from_server).encode('utf-8')
			# This loads the bytestream into a json_object
			json_object = json.loads(res_bytes)
			# This converts the json_object to a form that can be printed to the terminal (string)
			json_formatted_str = json.dumps(json_object, indent=2)
			# Print the nicely formatted json data to the terminal
			print("NOW PRINTING NICELY FORMATTED JSON WE RECEIVED FROM THE SERVER:")
			print(json_formatted_str)
		return r

	# this creates 2 files, one containing the names for all cfda nums in a given list of cfdas,
	# and another for the cfda nums for which the response was null
	def create_name_and_cfda_csv(self, csv_file_to_save, cfda_list_to_access=''):
		print("create name and cfda csv")
		spend_by_cat_body = {
			"filters": {
				"time_period": [
					{"start_date": "2012-10-01", "end_date": "2013-09-30"},
					{"start_date": "2013-10-01", "end_date": "2014-09-30"},
					{"start_date": "2014-10-01", "end_date": "2015-09-30"},
					{"start_date": "2015-10-01", "end_date": "2016-09-30"},
					{"start_date": "2016-10-01", "end_date": "2017-09-30"},
					{"start_date": "2017-10-01", "end_date": "2018-09-30"},
					{"start_date": "2007-10-01", "end_date": "2008-09-30"},
					{"start_date": "2018-10-01", "end_date": "2019-09-30"},
					{"start_date": "2008-10-01", "end_date": "2009-09-30"},
					{"start_date": "2019-10-01", "end_date": "2020-09-30"},
					{"start_date": "2009-10-01", "end_date": "2010-09-30"},
					{"start_date": "2020-10-01", "end_date": "2021-09-30"},
					{"start_date": "2010-10-01", "end_date": "2011-09-30"},
					{"start_date": "2011-10-01", "end_date": "2012-09-30"}
				],
				"program_numbers": [
					"10.001"
				]
			},
			"category": "cfda",
			"limit": 1,
			"page": 1
		}
		name_list_headers = ['CFDA', 'Name']
		self.cfda_and_name_list.append(name_list_headers)
		if cfda_list_to_access != '':
			temp_cfda_list = read_column_from_file(cfda_list_to_access)
		else:
			temp_cfda_list = self.cfda_num_list
		i = 0
		l = len(temp_cfda_list)
		temp_cfda_num = float(temp_cfda_list[0])
		print(temp_cfda_num)
		error_cfda_list = []

		while i < l:
			print("new loop: ", i)
			new_row = []
			spend_by_cat_body = self.update_request_body_cfda(temp_cfda_list[i], spend_by_cat_body)
			temp_resp = self.spending_by_category_cfda(
				spend_by_cat_body,
				display=False
			)
			# self.pretty_print_server_response()
			self.jsonify()
			new_row.append(temp_cfda_list[i])
			# print(new_row)
			if self.server_resp_json['results']:
				name = self.server_resp_json['results'][0]['name']
				# print("name: ", name)
				new_row.append(name)
				self.cfda_and_name_list.append(new_row)
			else:
				print("NAME ERROR, CFDA: ", temp_cfda_list[i])
				# self.pretty_print_server_response()
				new_row.append('NULL')
				error_cfda_list.append(temp_cfda_list[i])
				self.cfda_and_name_list.append(new_row)
			i += 1

		print("cfda and name list after loop: ", self.cfda_and_name_list)
		write_csv_list_to_file(self.cfda_and_name_list, csv_file_to_save)
		write_list_to_file(error_cfda_list, '../../data/TNC_CFDA_list/cfda_name_error_list.txt')

	def find_state_info(self, state, cfda_state_rank_list):
		state_name_abbrev = state
		new_row = []
		for row in cfda_state_rank_list:
			if row[2] == state_name_abbrev:
				new_row = row[4::]
		return new_row

	def washington_tnc_analysis(self, tnc_ref_csv_file, state_analysis_path, save_as_file):
		print("washington TNC analysis commencing...")
		tnc_data = read_csv(tnc_ref_csv_file)
		wp_cfda_list = read_column_from_file('../live/Updated_CFDA_list_noDuplicates.txt')
		# print("tnc data from file: ", tnc_data)
		print("wp cfda list: ", wp_cfda_list)
		tnc_data[0].insert(3, 'CFDA Name')
		tnc_data[0].insert(4, 'Total Spending')
		tnc_data[0].insert(5, 'Total Spending Rank')
		tnc_data[0].insert(6, 'Per Capita Spending')
		tnc_data[0].insert(7, 'Per Capita Spending Rank')
		tnc_data[0].insert(8, 'Awarding Sub Agency')
		tnc_data[0].insert(9, 'Unique from WP CFDA list?')
		print("\n\n\nNEW tnc data from file: ", tnc_data[0])
		final_list = []
		final_list.append(tnc_data[0])

		for row in tnc_data[1::]:
			print("cfda: ", row[2])
			try:
				temp_row = row
				for i in range(3, 10):
					temp_row.insert(i, 'X')
				cfda_info = read_csv(self.set_state_state_filename(row[2]))
				state_info_for_cfda = self.find_state_info('WA', cfda_info)
				print("state info for cfda: ", state_info_for_cfda)
				unique = 'TRUE'
				if row[2] in wp_cfda_list:
					unique = 'FALSE'
				# print("full row: ", row)
				'''
				temp_row = row[:3] + state_info_for_cfda + row[10::]
				temp_row[9] = unique'''
				print("temp row initial: ", temp_row)
				for i in range(6):
					temp_row[i + 3] = state_info_for_cfda[i]
				temp_row[9] = unique
				print("new row: ", temp_row)
				final_list.append(temp_row)


			except OSError:
				print("something went wrong")

		write_csv_list_to_file(final_list, save_as_file)

	def pull_records_by_county(self, county_ref_file):
		cfda_num_array = self.read_cfda_list_from_file('../../data/reference/TNC_working_cfda_list.txt')
		# print(cfda_num_array)
		county_ref_info = read_csv(county_ref_file)
		wp_category_info = read_csv('../../data/reference/TNC_list_all_yrs_WA_analysis - re-integrate.csv')

		# print("wp cat info: ", wp_category_info)
		print("county ref info: ", county_ref_info)
		url = self.make_url('spending_by_award')
		# print("body access testing: ", self.body['filters']['place_of_performance_locations'][0]['county'])
		# print("county ref access test: ", county_ref_info[1][1:3:])
		# we start at the first cfda
		current_cfda_index = 0
		current_county_index = 1
		county_list_length = len(county_ref_info)
		# make the first POST req
		# response_from_server = POST(url, body)
		# retrieve JSON from response
		# json_response = JSON_ify(response_from_server)
		# print(response_from_server.status_code)
		# update the cfda number we're working with right now
		curr_cfda_num = cfda_num_array[current_cfda_index]
		print(curr_cfda_num)
		# should be the first cfda number in the list
		curr_cfda_file = self.set_cfda_filename(curr_cfda_num)
		print(curr_cfda_file)
		# save the file initially
		# Write_CSV(json_response, curr_cfda_file)
		# length of list of cfda nums
		cfda_list_length = len(cfda_num_array)
		# loop control
		downloading = True
		# iterate pages, we start at 2 because the first req asked
		# for the first page of the first cfda num
		page_to_request = 1
		is_first_contact = True
		file_written = False
		counties_complete = False
		response_from_server = requests.models.Response()

		while downloading and current_cfda_index < cfda_list_length:

			if response_from_server.status_code == 200 or is_first_contact:
				if is_first_contact:
					is_first_contact = False
				response_from_server = self.post_req_newpage(url, page_to_request)
				self.jsonify()
				json_response = self.server_resp_json
				# print("\n\n json_response: ", json_response)
				# self.pretty_print_server_response()
				response_page = json_response['page_metadata']['page']
				has_next_page = json_response['page_metadata']['hasNext']
				# print("response page: ", response_page)

				if not file_written and json_response['results']:
					write_new_cfda_csv_file(
						json_response, curr_cfda_file,
						insert_list=county_ref_info[current_county_index][1:3:])
					# print("county info for file written: ", county_ref_info[current_county_index][1:3:])
					file_written = True

				elif file_written and json_response['results']:
					try:
						append_cfda_csv_file(
							json_response, curr_cfda_file,
							insert_list=county_ref_info[current_county_index][1:3:])
					except UnicodeEncodeError:
						print("unicode encode error")

				if has_next_page:
					downloading = True
					page_to_request += 1
				elif current_county_index <= county_list_length and not counties_complete:
					print("END OF COUNTY: ", county_ref_info[current_county_index])
					if not counties_complete:
						try:
							self.update_request_body_county(county_ref_info[current_county_index + 1][1])
							current_county_index += 1
							print("new county index: ", current_county_index)
						except IndexError:
							print("\n-----------------------ALL COUNTIES COMPLETE FOR THIS CFDA")
							counties_complete = True
					page_to_request = 1
				else:
					print("END OF CFDA:  ", curr_cfda_num)
					try:
						curr_cfda_num = cfda_num_array[current_cfda_index + 1]
						current_cfda_index += 1
						body = self.update_request_body_cfda(curr_cfda_num)
						curr_cfda_file = self.set_cfda_filename(curr_cfda_num)
						page_to_request = 1
						print("NEW CFDA: ")
						print(curr_cfda_num)
						current_county_index = 1
						file_written = False
						counties_complete = False
					except IndexError:
						print("\n--------- CFDA LIST COMPLETE ")
						break


			# if things did not go smoothly
			else:
				print("NOW PRINTING ENTIRE RESPONSE AS ERROR:")
				print(type(response_from_server))
				# This will print the entire response from the server, not just the JSON
				data = dump.dump_all(response_from_server)
				print(data.decode('utf-8'))
				files = data.decode('utf-8')
				downloading = False

	# sleep(1)

	def individual_county_check(self, cfda, county_fips):
		amount = 0.00
		self.update_request_body_county(county_fips)
		self.update_request_body_cfda(cfda)

		resp = self.post_req_newpage(self.make_url('spending_by_award'), 1)
		self.pretty_print_server_response()
		print("\n -----now for state only\n")

		for county in self.wa_county_names:
			print("county INFO: ", county, " ", county[1])
			self.update_request_body_county(county[1])
			resp = self.post_req_newpage(self.make_url('spending_by_award'), 1)
			self.jsonify()
			if self.server_resp_json['results']:
				# self.pretty_print_server_response()
				self.pretty_print_server_data()
				for entry in self.server_resp_json['results']:
					amount += float(entry['Award Amount'])
		print("TOTAL AMOUNT: ", amount)
		print("\n  Done with County Check")

	def analyze_county_data(
			self,
			county_ref_file='../../data/reference/WA FIPS + 2019 pop estimates - Sheet1.csv',
			cfda_county_breakdown_root='../../data/TNC_CFDA_list/WA_Counties/'):
		print(" analyze county data ")
		county_ref_info = read_csv(county_ref_file)
		wp_category_info = read_csv('../../data/reference/TNC_list_all_yrs_WA_analysis - re-integrate.csv')
		cfda_num_array = self.read_cfda_list_from_file('../../data/reference/TNC_working_cfda_list.txt')
		analyzed_county_breakdown = [['CFDA #']]
		for i in range(3, 7):
			analyzed_county_breakdown[0].append(wp_category_info[0][i])
		print("county breakdown: ", analyzed_county_breakdown)
		for county in county_ref_info[1::]:
			wp_category_info[0].append(county[2] + ', FIPS: ' + county[1] + ", Pop: " + county[3])
			wp_category_info[0].append(county[2] + ' Total Spending')
			wp_category_info[0].append(county[2] + ' Total Rank')
			wp_category_info[0].append(county[2] + ' Per Cap Spending')
			wp_category_info[0].append(county[2] + ' Per Cap Rank')

		for cfda_num in cfda_num_array[:2]:
			print("cfda num: ", cfda_num)
			curr_cfda_file_contents = read_csv(self.set_cfda_filename(cfda_num))
			#print("file cfda contents: ", curr_cfda_file_contents)

		#print("\n\nupdated headers: ", wp_category_info[0])