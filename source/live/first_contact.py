import csv
import requests
import json
from requests_toolbelt.utils import dump

# This is the name for the file where the data is saved, as well as the path
# The path specifies that the .txt files should be stored in the data/testing folder
# Also, text after a "#" sign won't be evaluated as code, they're comments
data_file_path = '../../data/testing/'
data_file_name = 'datafile_title.txt'
data_file = data_file_path + data_file_name

# This function saves a json 'list' to a file
# if you change the file name, a new file will be written
def save_json_to_file(data_to_write):
	with open(data_file, 'w') as outfile:
		json.dump(data_to_write, outfile, indent=2)
	outfile.close()


url = 'https://api.usaspending.gov/api/v2/recipient/state/'

# This is where we make a GET request to the server at the specified url
response_from_server = requests.get(url)
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

print("NOW PRINTING ENTIRE RESPONSE:")
# This will print the entire response from the server, not just the JSON
data = dump.dump_all(response_from_server)
print(data.decode('utf-8'))
files = data.decode('utf-8')
