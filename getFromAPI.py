import requests 
import json

url = "https://bostoncollege.instructure.com/api/v1/courses"
token = "1019~k35JVInSNkAYEQURpNNDiLPINKXD4vTv5bEiwWr0EAcdLRULy66ja4KSTYR3vauh"
headers = {"Authorization" : "Bearer {}".format(token)}
params = {"state[]" : "available"}

def extract():
	r = requests.get(url, headers = headers, params = params)

	with open('data.json', 'w') as json_file:
		json.dump(r.json()[0], json_file, indent = 1)


#  make sure to get the current time zone of the parse inorder
#  to change the time in the future