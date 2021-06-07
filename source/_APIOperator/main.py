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

if __name__ == "__main__":
	main()
	api = API()
	api.spending_by_category_cfda(body=spend_by_cat_body, display=True)
