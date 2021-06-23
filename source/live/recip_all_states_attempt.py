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
data_file_path = '../../data/TNC_CFDA_list/recipient_records_for_each_cfda/'
state_pops_file = '2019_state_pops_wAbbrevs.csv'
csv_file_name = 'CFDA_'
curr_cfda_file = data_file_path + csv_file_name
print(curr_cfda_file)


def read_csv(file):
	arr = []
	with open(file, newline='') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			arr.append(row)
	csvfile.close()
	return arr


def set_CFDA_filename(cfda):
	cfda_file = data_file_path + csv_file_name + str(cfda).replace('.', '') + '.csv'
	# print("now printing cfda file")
	# print(cfda_file)
	# print("done printing cfda file")
	return cfda_file


def make_file(file):
	data_file = open(file, 'w', newline='')
	data_file.close()


def Write_CSV(json_in, csv_file):
	print("WRITE CFDA (should be 1 per cfda)")
	print(csv_file)
	results = json_in['results']
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


def Append_CSV(json_in, csv_file):
	results = json_in['results']
	# now we will open a file for writing
	data_file = open(csv_file, 'a', newline='')
	# create the csv writer object
	csv_writer = csv.writer(data_file)
	# Counter variable used for writing
	# headers to the CSV file
	for res in results:
		csv_writer.writerow(res.values())
	data_file.close()


def Read_CFDA_Nums_From_File(file):
	arr = []
	with open(file, 'r') as f:
		arr = f.read().splitlines()
	f.close()
	# print(arr)
	return arr


def Pretty_Print_Response(resp):
	print("NOW PRINTING ENTIRE RESPONSE")
	data = dump.dump_all(resp)
	print(data.decode('utf-8'))


def JSON_ify(response_from_server):
	# This line extracts the JSON data out of the message we got from the server
	# Pretty_Print_Response(response_from_server)
	json_from_server = response_from_server.json()
	# This encodes it as a bytestream
	res_bytes = json.dumps(json_from_server).encode('utf-8')
	# This loads the bytestream into a json_object
	json_object = json.loads(res_bytes)
	# This converts the json_object to a form that can be printed to the terminal (string)
	json_formatted_str = json.dumps(json_object, indent=2)
	# Print the nicely formatted json data to the terminal
	# print("NOW PRINTING NICELY FORMATTED JSON WE RECEIVED FROM THE SERVER:")
	# print(json_formatted_str)
	# print("NICELY FORMATTED JSON IS DONE PRINTING")
	return json_from_server


def unicode_encode_award_ids(id):
	with open('unicode_encode_error_award_ids.txt', 'a', newline='') as log:
		log.write(id)
		log.write("\n")
	log.close()


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
	# print("REQUEST TO SERVER HAS BEEN MADE")
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
		"recipient_locations": [
			{
				"country": "USA",
				"state": "WA"
			}
		],
		"program_numbers": [
			"10.069"
		]
	},
	"fields": [
		"Award ID", "Recipient Name", "Award Amount", "Description", "def_codes", "Awarding Agency",
		"Awarding Sub Agency", "Award Type", "CFDA Number", "Place of Performance State Code",
		"Place of Performance Country Code", "Place of Performance Zip5", "Place of Performance City Code",
		"Contract Award Type", "Funding Agency Code", "Recipient DUNS Number", "Awarding Agency Code",
		"generated_internal_id"
	],
	"page": 1,
	"limit": 100,
	"sort": "Award Amount",
	"order": "desc",
	"subawards": False
}

cfda_num_array = Read_CFDA_Nums_From_File('../../data/reference/TNC_CFDA_list_formatted.txt')
# print(cfda_num_array)
# print(json.dumps(CFDA_body_update(body, cfda_num_array[0]), indent=2))

body = CFDA_body_update(body, cfda_num_array[0])

url = url_base + spend_by_award
current_cfda_index = 0
curr_cfda_num = cfda_num_array[current_cfda_index]
print(curr_cfda_num)

print(curr_cfda_file)
cfda_list_length = len(cfda_num_array)
# loop control
downloading = True
page_to_request = 1
is_first_contact = True
response_from_server = requests.models.Response()
pops_list = read_csv(state_pops_file)
award_code_sets = [
	[
		"02", "03", "04", "05"
	],
	[
		"10", "06"
	]
]
new_cfda = True
curr_cfda_num = '10.923'
curr_cfda_file = set_CFDA_filename(curr_cfda_num)
body = CFDA_body_update(body, curr_cfda_num)

while current_cfda_index < cfda_list_length:

	for state in pops_list[1::]:
		body['filters']['recipient_locations'][0]['state'] = state[2]
		print(state[2], end=' ')
		downloading = True
		for awards in award_code_sets:
			body['filters']['award_type_codes'] = awards
			#print(awards)
			downloading = True
			while downloading:
				response_from_server = POST_for_new_page(url, body, page_to_request)
				#Pretty_Print_Response(response_from_server)
				json_response = JSON_ify(response_from_server)
				response_page = json_response['page_metadata']['page']
				has_next_page = json_response['page_metadata']['hasNext']
				# print("response page: ", response_page)

				if json_response['results']:
					print(json_response['results'][0]['Place of Performance State Code'])
					if not json_response['results'][0]['Place of Performance State Code']:
						json_response['results'][0]['Place of Performance State Code'] = state[2]
				if new_cfda:
					try:
						Write_CSV(json_response, curr_cfda_file)
					except UnicodeEncodeError:
						print("unicode encode error")
					new_cfda = False
				elif not new_cfda:
					try:
						#print("APpEND")
						Append_CSV(json_response, curr_cfda_file)
					except UnicodeEncodeError:
						print("unicode encode error")

				if has_next_page:
					downloading = True
					page_to_request += 1
				else:
					downloading = False
					page_to_request = 1
			# if things did not go smoothly

	new_cfda = True
	current_cfda_index += 1
	curr_cfda_num = cfda_num_array[current_cfda_index]
	print("\nnew cfda: ", curr_cfda_num)
	body = CFDA_body_update(body, curr_cfda_num)
	curr_cfda_file = set_CFDA_filename(curr_cfda_num)
	print(curr_cfda_file)

print("DONE")
