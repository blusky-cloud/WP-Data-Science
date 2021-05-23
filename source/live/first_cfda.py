import csv
import requests
import json
from requests_toolbelt.utils import dump

# This is the name for the file where the data is saved, as well as the path
# The path specifies that the .txt files should be stored in the data/testing folder
# Also, text after a "#" sign won't be evaluated as code, they're comments
# This only works if you have data and testing folders like in this repository
# If you're running this locally, just keep the name in the save_json_to_file function
# As "data_file_name" and it will save in whatever folder the python script is stored
data_file_path = '../../data/testing/'
data_file_name = 'cfda_10-664_by_award.txt'
data_file = data_file_path + data_file_name # will error without data and testing folders

# This function saves a json 'list' to a file
# if you change the file name, a new file will be written
def save_json_to_file(data_to_write):
	with open(data_file, 'w') as outfile:
		json.dump(data_to_write, outfile, indent=2)
	outfile.close()

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
			"10.664"
		]
	},
	"fields": [
		"Award ID", "Recipient Name", "Start Date", "End Date", "Award Amount", "Description", "def_codes",
		"COVID-19 Obligations", "COVID-19 Outlays", "Awarding Agency", "Awarding Sub Agency", "Award Type",
		"recipient_id", "prime_award_recipient_id", "CFDA Number"
	],
	"page": 1,
	"limit": 100,
	"sort": "Award Amount",
	"order": "desc",
	"subawards": False
}
url = url_base + spend_by_award
headers = {'Content-Type': 'application/json'}
payload = body

response_from_server = requests.post(url, headers=headers, json=payload)

print("NOW PRINTING ENTIRE RESPONSE:")
# This will print the entire response from the server, not just the JSON
data = dump.dump_all(response_from_server)
print(data.decode('utf-8'))
files = data.decode('utf-8')
# This is where we make a GET request to the server at the specified url

print("REQUEST TO SERVER HAS BEEN MADE")

# This line extracts the JSON data out of the message we got from the server
json_from_server = response_from_server.json()

# This encodes it as a bytestream
res_bytes = json.dumps(json_from_server).encode('utf-8')
# This loads the bytestream into a json_object
json_object = json.loads(res_bytes)
# This converts the json_object to a form that can be printed to the terminal (string)
json_formatted_str = json.dumps(json_object, indent=2)
# Print the nicely formatted json data to the terminal
print("NOW PRINTING NICELY FORMATTED JSON WE RECEIVED FROM THE SERVER:")
print(json_formatted_str)
print("NICELY FORMATTED JSON IS DONE PRINTING")

# here is the function call to save data to a file
save_json_to_file(json_from_server)
print("DATA SAVED TO FILE")


print("DONE")