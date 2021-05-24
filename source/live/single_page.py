import csv
import requests
import json
from requests_toolbelt.utils import dump
from time import sleep

# This is the name for the file where the data is saved, as well as the path
# The path specifies that the .txt files should be stored in the data/testing folder
# Also, text after a "#" sign won't be evaluated as code, they're comments
# This only works if you have data and testing folders like in this repository
# If you're running this locally, just keep the name in the save_json_to_file function
# As "data_file_name" and it will save in whatever folder the python script is stored
data_file_path = '../../data/testing/'
data_file_name = 'single_page1.txt'
csv_file_name = 'single_page1_csv.csv'
data_file = data_file_path + data_file_name  # will error without data and testing folders
csv_file = data_file_path + csv_file_name

def Write_CSV(json_in):

	results = json_in['results']
	# now we will open a file for writing
	data_file = open(csv_file, 'w')
	# create the csv writer object
	csv_writer = csv.writer(data_file)
	# Counter variable used for writing
	# headers to the CSV file
	count = 0
	for res in results:
		if count == 0:
			# Writing headers of CSV file
			header = res.keys()
			csv_writer.writerow(header)
			count += 1

		# Writing data of CSV file
		csv_writer.writerow(res.values())

	data_file.close()

def Append_CSV(json_in):
	results = json_in['results']
	# now we will open a file for writing
	data_file = open(csv_file, 'w')
	# create the csv writer object
	csv_writer = csv.writer(data_file)
	# Counter variable used for writing
	# headers to the CSV file
	count = 0
	for res in results:
		if count == 0:
			# Writing headers of CSV file
			header = res.keys()
			csv_writer.writerow(header)
			count += 1

		# Writing data of CSV file
		csv_writer.writerow(res.values())

	data_file.close()

def Read_CFDA_Nums_From_File(file):
	with open(file) as f:
		array = []
		d = {}
		for line in f:  # read rest of lines
			array.append(float(line))
	return array

# This function saves a json 'list' to a file
# if you change the file name, a new file will be written
def save_json_to_file(data_to_write):
	with open(data_file, 'w') as outfile:
		json.dump(data_to_write, outfile, indent=2)
	outfile.close()


def Append_comma():
	with open(data_file, 'a') as outfile:
		outfile.write(',')
	outfile.close()


def Append_json_to_file(data_to_write):
	with open(data_file, 'a') as outfile:
		json.dump(data_to_write, outfile, indent=2)
	outfile.close()

def Pretty_Print_Response(resp):
	print("NOW PRINTING ENTIRE RESPONSE")
	data = dump.dump_all(resp)
	print(data.decode('utf-8'))


def JSON_ify(response_from_server):
	# This line extracts the JSON data out of the message we got from the server
	json_from_server = response_from_server.json()
	# This encodes it as a bytestream
	res_bytes = json.dumps(json_from_server).encode('utf-8')
	# This loads the bytestream into a json_object
	json_object = json.loads(res_bytes)
	# This converts the json_object to a form that can be printed to the terminal (string)
	json_formatted_str = json.dumps(json_object, indent=2)
	# Print the nicely formatted json data to the terminal
	#print("NOW PRINTING NICELY FORMATTED JSON WE RECEIVED FROM THE SERVER:")
	#print(json_formatted_str)
	#print("NICELY FORMATTED JSON IS DONE PRINTING")
	return json_from_server


def POST(url, body):
	headers = {'Content-Type': 'application/json'}
	payload = body
	resp = requests.post(url, headers=headers, json=payload)
	print("REQUEST TO SERVER HAS BEEN MADE")
	return resp


def POST_for_new_page(url, body, page):
	headers = {'Content-Type': 'application/json'}
	body['page'] = page
	payload = body
	resp = requests.post(url, headers=headers, json=payload)
	#print("REQUEST TO SERVER HAS BEEN MADE")
	return resp


def CFDA_body_update(bdy, cf):
	bdy['filters']['program_numbers'][0] = json.dumps(cf)
	return bdy


url_base = 'https://api.usaspending.gov'
state_1_url = '/api/v2/recipient/state/'
cfda_all_totals_url = '/api/v2/references/cfda/totals/'
# cfda_specific_url = '/api/v2/references/cfda/totals//'
cfda_specific_url = '/api/v2/references/cfda/totals/10.069/'
spend_by_award = "/api/v2/search/spending_by_award/"

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
			"10.069"
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

cfda_num_array = Read_CFDA_Nums_From_File('CFDA_nums.txt')
#print(cfda_num_array)
#print(json.dumps(CFDA_body_update(body, cfda_num_array[1]), indent=2))

cfda_list_length = len(cfda_num_array)

url = url_base + spend_by_award

response_from_server = POST(url, body)
json_response = JSON_ify(response_from_server)

print(type(json_response))
Write_CSV(json_response)
#save_json_to_file(json_response)
print("FIRST CONTACT MADE")

downloading = True
page_to_request = 1
current_cfda_index = 1


print("DONE")
