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

check_body = {
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
		"award_type_codes": ["02", "03", "04", "05"],
		"program_numbers": ["10.923"]
	},
	"fields": [
		"Award ID", "Recipient Name", "Start Date", "End Date", "Award Amount", "Description",
		"def_codes", "COVID-19 Obligations", "COVID-19 Outlays", "Awarding Agency",
		"Awarding Sub Agency", "Award Type", "recipient_id", "prime_award_recipient_id"
	],
	"page": 1, "limit": 60, "sort": "Award Amount", "order": "desc", "subawards": False
}

tnc_path_root = '../../data/TNC_CFDA_list/'
reference_path_root = '../../data/reference/'
cfda_list_file = reference_path_root + '/TNC_CFDA_list_formatted.txt'
tnc_cfda_names_list_file = tnc_path_root + '/TNC_CFDA_Names.csv'
if __name__ == "__main__":
	main()
	api = API()
	print("-----------------------MAIN-------------------------")
	# api.pull_records_by_county(reference_path_root + 'WA FIPS + 2019 pop estimates - Sheet1.csv')
	# api.individual_county_check('10.072', '001')
	# api.analyze_county_data()
	# api.washington_tnc_analysis(reference_path_root + 'TNC_list_all_yrs_WA_analysis - re-integrate.csv', 'WA_analysis_firstline_bug_fixed.csv')
	api.test_request(b=check_body)
