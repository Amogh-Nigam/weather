from django.test import TestCase

# Create your tests here.
import requests
import sys

import json

response = requests.request("GET",
                            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/delhi/next7days?unitGroup=metric&include=days&key=ZSQMPB72Y29QCJR67UK4XL2ZN&contentType=json")
if response.status_code != 200:
    print('Unexpected Status code: ', response.status_code)
    sys.exit()

# Parse the results as JSON
jsonData = response.json()

with open('data.json', 'w') as outfile:
    json.dump(jsonData, outfile, indent=4)
