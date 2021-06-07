import csv
import requests
import json
from requests_toolbelt.utils import dump


def read_column_from_file(file):
	with open(file, 'r') as f:
		num_list = f.read().splitlines()
	f.close()
	return num_list
