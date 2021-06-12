import perCapita_each_cfda as p

state_rankings_file_path = '../../data/analysis/State/'
state_name = 'Washington'
state_name_abbrev = 'WA'
state_cfda_rankings_file = state_rankings_file_path + state_name + '_' + state_name_abbrev + '_rankings.csv'


def find_washington_info(state_list, w_list):
	new_row = []
	for row in state_list:
		if row[2] == state_name_abbrev:  # if state abbrev. column is washington
			new_row.append(row[3])
			new_row.append(row[4])
			new_row.append(row[5])
			new_row.append(row[6])
			new_row.append(row[7])
			new_row.append(row[8])

			print("new_row: ", new_row)
			w_list.append(new_row)
	return w_list


# -------------------------------------------------
#     DO STUFF HERE
# -------------------------------------------------

print("Performing Analysis for Washington...")

cfda_index = 0
cfda_array = p.Read_CFDA_Nums_From_File(p.cfda_list_file)
#  print(cfda_file_contents)
print("--------------------------------------------------")
washington_list = [
	[
		'CFDA', 'CFDA Name', 'Total Spending',
		'Total Spending Rank', 'Per Capita Spending', 'Per Capita Spending Rank'
	]
]
print(washington_list[0])
index = 0

while index < len(cfda_array):
	print(cfda_array[index])
	cfda_state_contents = p.read_csv(p.set_state_CFDA_filename(cfda_array[index]))
	#  print(cfda_state_contents)

	washington_list = find_washington_info(cfda_state_contents, washington_list)
	#  print("created washington row: ", washington_list)
	index += 1

print("--------------------------------------------------")
print("washington list: ", washington_list)
p.Write_CSVList(washington_list, state_cfda_rankings_file)
