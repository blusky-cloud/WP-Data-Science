import csv
import requests
import json
from requests_toolbelt.utils import dump


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
					"state": "OR",
					"county": "001"
				}
			],
			"program_numbers": [
				"10.001"
			]
		},
		"fields": [
			"Award ID", "Recipient Name", "Start Date", "End Date", "Award Amount", "Description", "def_codes",
			"COVID-19 Obligations", "COVID-19 Outlays", "Awarding Agency", "Awarding Sub Agency", "Award Type",
			"recipient_id", "prime_award_recipient_id", "CFDA Number", "Place of Performance State Code",
			"Place of Performance Country Code", "Place of Performance Zip5"
		],
		"page": 1,
		"limit": 100,
		"sort": "Award Amount",
		"order": "desc",
		"subawards": False
	}
	cfda_num_list = []

	def __init__(self, b=None, cfda_list_file=''):
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

	def __str(self):
		print("BODY: ", self.body)

	def make_url(self, endpoint):
		return self.url_root + self.api[endpoint]

	def read_cfda_list_from_file(self, file):
		with open(file, 'r') as f:
			self.cfda_num_list = f.read().splitlines()
		f.close()
		return self.cfda_num_list

	def update_request_body_cfda(self, cfda):
		self.body['filters']['program_numbers'][0] = json.dumps(cfda)
		return self.body

	def post_request(self, endpoint):
		headers = {'Content-Type': 'application/json'}
		payload = self.body
		self.response_from_server = requests.post(self.make_url(endpoint), headers=headers, json=payload)
		return self.response_from_server

	def post_req_newpage(self, endpoint, page):
		headers = {'Content-Type': 'application/json'}
		self.body['page'] = page
		payload = self.body
		self.response_from_server = requests.post(self.make_url(endpoint), headers=headers, json=payload)
		return self.response_from_server

	def pretty_print_server_response(self):
		print("NOW PRINTING ENTIRE RESPONSE")
		data = dump.dump_all(self.response_from_server)
		print(data.decode('utf-8'))

	def test_request(self):
		self.post_request('all_cfda_totals')
		self.pretty_print_server_response()

	# this response includes the names for the cfda nums
	def spending_by_category_cfda(self, body={}, display=True):
		print("spending by cat: cfda")
		headers = {'Content-Type': 'application/json'}
		payload = body
		print(f"body: {body}")
		api_name = "spending_by_category_cfda"
		url_api = self.make_url(api_name)
		print(f"url_api: {url_api}")
		r = requests.post(url_api, headers=headers, json=payload)
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