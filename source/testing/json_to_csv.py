import json
import csv

# Opening JSON file and loading the data
# into the variable data

json_file_path = "../../../../Data/CFDA_full_range_JSON_may23-2021.txt"
test_json_path = "../../data/testing/all_cfda_in_list_2_formatted.txt"

csv_file_path = "../../../../Data/CFDA_full_range_CSV_may23-2021.csv"
test_csv_path = "../../data/testing/all_cfda_in_list_2_formatted_CSV.csv"


with open(test_json_path) as json_file:
	data = json.load(json_file)

results = data['CFDA_RANGE']

# now we will open a file for writing
data_file = open(test_csv_path, 'w')

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