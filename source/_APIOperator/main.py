from __init__ import APIOperator as API


def main():
	print("Running Main")


# ------------------------------------------------------------------------------
#                     DO STUFF HERE
# ------------------------------------------------------------------------------
spend_by_cat_body = {
	"filters": {
		"time_period": [
			{
				"start_date": "2019-09-28",
				"end_date": "2020-09-28"
			}
		],
		"program_numbers": [
			"10.001"
		]
	},
	"category": "cfda",
	"limit": 100,
	"page": 1
}

tnc_path_root = '../../data/TNC_CFDA_list/'
reference_path_root = '../../data/reference/'
cfda_list_file = reference_path_root + '/TNC_CFDA_list_formatted.txt'
tnc_cfda_names_list_file = tnc_path_root + '/TNC_CFDA_Names.csv'
if __name__ == "__main__":
	main()
	api = API()
	print("-----------------------MAIN-------------------------")
	#api.pull_records_by_county(reference_path_root + 'WA FIPS + 2019 pop estimates - Sheet1.csv')
	#api.individual_county_check('10.072', '001')
	api.analyze_county_data()