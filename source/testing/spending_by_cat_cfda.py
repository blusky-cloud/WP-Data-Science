# https://lulstrup.medium.com/gaining-an-analytics-edge-using-federal-spending-open-data-b91b517f2c04

import os, glob
import pandas as pd
import requests
import bs4
import json
import time
from datetime import datetime
import zipfile
import pprint
import csv
import numpy as np
from requests_toolbelt.utils import dump

data_file_path = '../../data/testing/'
data_file_name = 'cfda_response_1.txt'
data_file = data_file_path + data_file_name  # will error without data and testing folders


# This function saves a json 'list' to a file
# if you change the file name, a new file will be written
def save_json_to_file(data_to_write):
	with open(data_file, 'w') as outfile:
		json.dump(data_to_write, outfile, indent=2)
	outfile.close()


def Convert_Newlines_To_Commas(i_file):
	print("converting...")
	with open(i_file) as f:
		o_array = []
		for line in f:
			o_array.append(float(line))
	print(type(o_array))
	'''
	np_arr = np.array(o_array, dtype=np.float32)
	np.savetxt('cfda_nums_csv.csv', [np_arr], delimiter=',', fmt='%d')
	print(np_arr)
	'''
	with open('new_cfda_csv.csv', "wb") as file:
		writer = csv.writer(file)
		writer.writerow(o_array)


def Get_String_From_CFDA(cfda):
	str_cfda = cfda.replace("\'", "\"")
	str_cfda = str_cfda.replace("\\n", "")
	return str_cfda


def Read_CFDA_Nums_From_File(file):
	with open(file) as f:
		array = []
		d = {}
		for line in f:  # read rest of lines
			array.append(str(line))
	return array


def Enhance_Spending_File(df):
	df = df.fillna("UNSPECIFIED")  # IMPORTANT - NA fields can affect groupby sums and other problems
	df['PSC_Cat'] = df['product_or_service_code'].str[:1]
	df['PSC_Cat_2'] = df['product_or_service_code'].str[:2]
	return df


def Type_Print_Unknown(unknown):
	print("----Find Type and Print Object----")
	print(type(unknown))

	if type(unknown) == dict:
		pprint.pprint(unknown)
	else:
		try:
			print(unknown)
		except:
			print(" couldn't print unknown ")


def Get_API_Github_Definition(url_test_api):
	pass
	# need to use selenium to get the "here" link to github code
	return


# TEST
Get_API_Github_Definition(
	"https://api.usaspending.gov/api/v2/award_spending/recipient/?fiscal_year=2016&awarding_agency_id=183")


def Get_API_Endpoints():
	url_root = "https://api.usaspending.gov"
	r = requests.get("https://api.usaspending.gov/docs/endpoints")
	# r.content
	soup = bs4.BeautifulSoup(r.content, features="html.parser")
	results_list = []
	table = soup.find('table')
	thead = table.find('thead').find('tr')
	#     for header in thead:
	#         print(header)
	#         # gather header titles
	for tr in table.find_all('tr'):
		elements = []
		for td in tr.find_all('td'):
			for a in td.find_all('a'):
				try:
					elements.append(url_root + a['href'])
				# print("...", a['href']) #, a['href'])
				except:
					pass
			# print(a)
			# print(td.text)
			elements.append(td.text)
		if elements:
			results_list.append({'url_test_api': elements[0], 'Endpoint': elements[1], 'Methods': elements[2],
								 'Description': elements[3]})
	# print()
	df = pd.DataFrame(results_list)
	df['Endpoint_Labels'] = df['Endpoint'].apply(lambda x: "_".join(x.split("/")[3:])[0:-1])
	return df


# -----------------------------------------------------------------------------------------------------------
# CLASS USAspending()


class USAspending():
	# TODO: refactor and simplify the code (the code in several of the methods is redundant and should be streamlined) for maintainability
	# TODO: add more tests to confirm it is working correctly and reliably

	url_root = 'https://api.usaspending.gov'  # !! note it is api.usaspending.gov NOT www.usaspending.gov
	api = {}
	api['parent_child'] = '/api/v2/recipient/children/'  # '/DUNS'
	api['recipient_spending_category'] = '/api/v2/search/spending_by_category/recipient_duns/'
	api['recipient_overview'] = "/api/v2/recipient/duns/"
	api['autocomplete_psc'] = "/api/v2/autocomplete/funding_psc/"
	api['autocomplete_funding_agency'] = "/api/v2/autocomplete/funding_agency/"
	api['autocomplete_glossary'] = "/api/v2/autocomplete/glossary/"
	api['bulk_download_awards'] = "/api/v2/bulk_download/awards/"
	api['bulk_download_list_agencies'] = "/api/v2/bulk_download/list_agencies/"
	api['bulk_download_status'] = "/api/v2/bulk_download/status/"
	api['spending_by_category_cfda'] = "/api/v2/search/spending_by_category/cfda/"

	USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
	USER_AGENT = "XY"  # solves 406 error on redirect of the biden mailer click link #
	headers = {"user-agent": USER_AGENT}

	def __init__(self, ):
		pass  # this __init__ can include variables set up at the creation of the object for this class, TBD

	def Get_URL_API(self, api_name, contents=""):
		if contents == '':
			return self.url_root + self.api[api_name]
		else:
			return self.url_root + self.api[api_name] + contents + '/'

	def API_Check_Status(self, requests_response):
		# print(requests_response)
		if requests_response.status_code == 200:
			return json.loads(requests_response.content)
		else:
			return "Error - response:", requests_response.status_code, requests_response.reason

	def API_Get_Parent_Child_Details_Using_DUNS(self, aDUNS):

		api_name = 'parent_child'
		url_api = self.Get_URL_API(api_name, contents=aDUNS)
		# print(url_api)
		r = requests.get(url_api)
		# print(r)

		return self.API_Check_Status(r)

	def API_Overview_Recipient_ID(self, recipient_id):

		api_name = 'recipient_overview'
		url_api = self.Get_URL_API(api_name, contents=recipient_id)

		# print(url_api)
		r = requests.get(url_api, headers=self.headers)
		# print(r)
		return self.API_Check_Status(r)

	def API_Name_Search(self, pattern):
		print("...querying USAspending.gov API...")

		api_name = 'recipient_spending_category'
		url_api = self.Get_URL_API(api_name)

		# print(url_api)
		page = 1
		next_page = True

		results = []

		while next_page:
			print(f'page:{page}', end=",")
			payload = {"page": page, "filters": {"recipient_search_text": [pattern]}}
			r = requests.post(url_api, json=payload)  # note this is a POST
			# print(r)
			result_record = self.API_Check_Status(r)
			results.append(result_record)

			# insert code here (turn it into a function) that keeps reading pages until 'hasNext' == False
			page += 1
			next_page = result_record['page_metadata']['hasNext']

		self.name_search_results = results

		return self.API_Check_Status(r)

	def Autocomplete_psc(self, search_text):
		return

	def Autocomplete_funding_agency(self, search_text):
		headers = {'Content-Type': 'application/json'}
		payload = {'search_text': search_text}
		api_name = 'autocomplete_funding_agency'
		url_api = self.Get_URL_API(api_name)
		r = requests.post(url_api, headers=headers, json=payload)
		return self.API_Check_Status(r)

	def Autocomplete_glossary(self, search_text):
		payload = {'search_text': search_text}
		api_name = 'autocomplete_glossary'
		url_api = self.Get_URL_API(api_name)
		r = requests.post(url_api, json=payload)
		return self.API_Check_Status(r)

	def Bulk_Download(self, body={}):
		headers = {'Content-Type': 'application/json'}
		payload = body
		print(f"body: {body}")
		api_name = "bulk_download_awards"
		url_api = self.Get_URL_API(api_name)
		print(f"url_api: {url_api}")

		r = requests.post(url_api, headers=headers, json=payload)
		return self.API_Check_Status(r)

	def CFDA_Category(self, body={}):
		headers = {'Content-Type': 'application/json'}
		payload = body
		print(f"body: {body}")
		api_name = "spending_by_category_cfda"
		url_api = self.Get_URL_API(api_name)
		print(f"url_api: {url_api}")

		r = requests.post(url_api, headers=headers, json=payload)
		return r

	def Bulk_Download_list_agencies(self, body={}):
		headers = {'Content-Type': 'application/json'}
		payload = body
		print(f"body: {body}")
		api_name = "bulk_download_list_agencies"
		url_api = self.Get_URL_API(api_name)
		print(f"url_api: {url_api}")

		r = requests.post(url_api, headers=headers, json=payload)
		return self.API_Check_Status(r)

	def Bulk_Download_status(self, body={}):
		headers = {'Content-Type': 'application/json'}
		payload = body
		print(f"body: {body}")
		api_name = 'bulk_download_status'
		url_api = self.Get_URL_API(api_name) + "?file_name=" + body['file_name']
		print(f"url_api: {url_api}")

		r = requests.get(url_api)  # ! GET not POST
		return self.API_Check_Status(r)

	def API_Process_POST_Response(self, api_post_json):

		return_value = []
		# print(api_post_json.keys())
		next_page = api_post_json['page_metadata']['hasNext']  # !!!TODO change this to handle MULTIPLE Pages
		results = api_post_json['results']
		print(f"results:{results}")
		parent_id_list = []
		for recipient in results:
			info_record = self.API_Overview_Recipient_ID(recipient['recipient_id'])
			return_value.append(info_record)
			if info_record['parent_id']:  # adds the parent to the records returned

				if not info_record['parent_id'] in parent_id_list:
					return_value.append(self.API_Overview_Recipient_ID(info_record['parent_id']))
					parent_id_list.append(info_record['parent_id'])

		return pd.DataFrame(return_value)


# END CLASS
# -----------------------------------------------------------------------------------------------------------
# DO STUFF
print("  NOW DOING STUFF ")
'''
print("NOW RUNNING GET ENDPOINTS")
df_api_endpoints = Get_API_Endpoints()
print(df_api_endpoints)
print( type(df_api_endpoints) )
pd.DataFrame.to_html(df_api_endpoints)
'''

spending = USAspending()
cfda_nums = Read_CFDA_Nums_From_File('CFDA_nums.txt')
Type_Print_Unknown(cfda_nums)
'''
for c in cfda_nums:
	c = c.replace("\'", "\"")
	c = c.replace("\n", "")
	'''

body = {
	"filters": {
		"prime_award_types": [
			"IDV_A",
			"IDV_B",
			"IDV_B_A",
			"IDV_B_B",
			"IDV_B_C",
			"IDV_C",
			"IDV_D",
			"IDV_E",
			"02",
			"03",
			"04",
			"05",
			"06",
			"07",
			"08",
			"09",
			"10",
			"11",
			"A",
			"B",
			"C",
			"D",
		],
		"program_numbers": [
			"10.069", "10.46", "10.664"
		],
		"date_range": {
			"start_date": "2018-10-01",
			"end_date": "2019-09-30"
		},
		"date_type": "action_date"
	}
}

json_body = json.loads(json.dumps(body))
list_json = cfda_nums
print(type(json_body))

json_body["filters"]["program_numbers"] = list_json
Type_Print_Unknown(json_body)
# body = json_body

'''
i=0
while i<len(cfda_nums):
	str_to_append = "\"" + str(cfda_nums[i]) + "\""
	body["filters"]["program_numbers"].append(str_to_append)
	i+=1
'''

# Convert_Newlines_To_Commas("CFDA_nums.txt")

# with open(download_file_name, 'wb') as output:
#	output.write(r.content)

print("---NOW REQ BULK DOWNLOAD---")
download_info = spending.Bulk_Download(body=body)
Type_Print_Unknown(download_info)

download_file_name = download_info['file_name']

body = {
	'file_name': download_file_name
}

print("---NOW GET DOWNLOAD STATUS---")
download_status = spending.Bulk_Download_status(body=body)

print("--- NOW WE WAIT UNTIL THE BULK DOWNLOAD IS PREPARED")

while download_status['status'] != 'finished':
	print(datetime.now(), download_file_name, download_status['status'],
		  f"elapsed seconds: {download_status['seconds_elapsed']}")
	print('...sleeping...')
	time.sleep(20)
	download_status = spending.Bulk_Download_status(body=body)

if download_status['status'] == 'finished':
	print(" -- download ready ---")

print("---GETTING DOWNLOAD---")
r = requests.get(download_info['file_url'], allow_redirects=True)

with open(download_file_name, 'wb') as output:
	output.write(r.content)

'''
json_from_server = response_from_server.json()
res_bytes = json.dumps(json_from_server).encode('utf-8')

# This loads the bytestream into a json_object
json_object = json.loads(res_bytes)
# This converts the json_object to a form that can be printed to the terminal (string)
json_formatted_str = json.dumps(json_object, indent=2)
# Print the nicely formatted json data to the terminal
print("NOW PRINTING NICELY FORMATTED JSON WE RECEIVED FROM THE SERVER:")
print(json_formatted_str)
print("NICELY FORMATTED JSON IS DONE PRINTING")
save_json_to_file(json_from_server)
print("DATA SAVED TO FILE")
print("NOW PRINTING ENTIRE RESPONSE:")
# This will print the entire response from the server, not just the JSON
data = dump.dump_all(response_from_server)
print(data.decode('utf-8'))
files = data.decode('utf-8')
'''