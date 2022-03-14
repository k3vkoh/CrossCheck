import requests 
import json

# url = "https://bostoncollege.instructure.com/api/v1/users/1614511/courses/:course_id/assignments"
url = "https://bostoncollege.instructure.com/api/v1/users/1614511/courses/:course_id/assignments"
# url = "https://bostoncollege.instructure.com/api/v1/courses/1631325/assignment_groups?exclude_assignment_submission_types%5B%5D=wiki_page&exclude_response_fields%5B%5D=description&exclude_response_fields%5B%5D=rubric&include%5B%5D=assignments&include%5B%5D=discussion_topic&override_assignment_dates=true&per_page=50"
token = "1019~JKjz2gIwQxZ9U6sf2cSjiKBOMBnt4zYEgZgH04ZUEZ2xKy0xKEdrmJkHqzqLAocR"

headers = {"Authorization" : "Bearer {}".format(token)}
params = {"state[]" : "available"}

def extract():
	r = requests.get(url, headers = headers, params = params)
	# r = requests.get(url)
	print(r)

	with open('data.json', 'w') as json_file:
		json.dump(r.json(), json_file, indent = 1)



#  make sure to get the current time zone of the parse inorder
#  to change the time in the future
