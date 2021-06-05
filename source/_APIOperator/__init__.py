import csv
import requests
import json
from requests_toolbelt.utils import dump


class APIOperator(object):
	url_root = 'https://api.usaspending.gov'
	api = {'spending_by_award': '/api/v2/search/spending_by_award/'}
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
			"program_numbers": [
				"10.001"
			],
			"place_of_performance_locations": [
				{
					"country": "USA",
					"county": "53001",
					"state": "WA"
				}
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

	def __init__(self, b=None):
		print(" initiating APIOperator ")
		if b is not None:
			self.body = b
		self.downloading = True
		self.page_to_request = 1
		self.is_first_contact = True
		self.curr_cfda_list_index = 0
		self.response_from_server = requests.models.Response()

	def __str(self):
		print("BODY: ", self.body)

	def make_url(self, endpoint):
		return self.url_root + self.api[endpoint]

	def req_year(self, year):


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
		resp = requests.post(self.make_url(endpoint), headers=headers, json=payload)
		return resp

	def post_req_newpage(self, endpoint, page):
		headers = {'Content-Type': 'application/json'}
		self.body['page'] = page
		payload = self.body
		resp = requests.post(self.make_url(endpoint), headers=headers, json=payload)
		return resp
