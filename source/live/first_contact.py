import csv
import requests
import json
from requests_toolbelt.utils import dump


url = 'https://api.usaspending.gov/api/v2/recipient/state/'

resp = requests.get(url)
print("get req made")


something = resp.json()
print(something)

json_data = '[{"ID":10,"Name":"Pankaj","Role":"CEO"},' \
            '{"ID":20,"Name":"David Lee","Role":"Editor"}]'

res_bytes = json.dumps(something).encode('utf-8')

json_object = json.loads(res_bytes)

json_formatted_str = json.dumps(json_object, indent=2)

print(json_formatted_str)



data = dump.dump_all(resp)

print(data.decode('utf-8'))
files = data.decode('utf-8')