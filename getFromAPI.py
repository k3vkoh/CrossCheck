import requests 
import json

token = "1019~JKjz2gIwQxZ9U6sf2cSjiKBOMBnt4zYEgZgH04ZUEZ2xKy0xKEdrmJkHqzqLAocR"

headers = {"Authorization" : "Bearer {}".format(token)}
params = {"state[]" : "all"}

my_courses = [1630778, 1631956, 1628579, 1631190]

def extract(my_courses):
	final_sch = {}
	# my_courses = [1628579]
	for course in my_courses:
		assignments = []

		# url = "https://bostoncollege.instructure.com/api/v1/courses/{}/assignments".format(str(course))
		# url = "https://bostoncollege.instructure.com/api/v1/courses/{}/assignment_groups".format(str(course))
		url = "https://bostoncollege.instructure.com/api/v1/courses/{}/assignment_groups?exclude_assignment_submission_types%5B%5D=wiki_page&exclude_response_fields%5B%5D=description&exclude_response_fields%5B%5D=rubric&include%5B%5D=assignments&include%5B%5D=discussion_topic&override_assignment_dates=true&per_page=50".format(str(course))

		r = requests.get(url, headers = headers, params = params)

		assignment_groups = r.json()
		for group in assignment_groups:
			for assignment in group["assignments"]:
				assignments.append({"name" : assignment["name"], "due": assignment["due_at"]})
		final_sch[course] = assignments
		print(r)



	with open('data.json', 'w') as json_file:
		json.dump(final_sch, json_file, indent = 1)
		# json.dump(r.json(), json_file, indent = 1)








# url = "https://bostoncollege.instructure.com/api/v1/courses/1631325/assignment_groups?exclude_assignment_submission_types%5B%5D=wiki_page&exclude_response_fields%5B%5D=description&exclude_response_fields%5B%5D=rubric&include%5B%5D=assignments&include%5B%5D=discussion_topic&override_assignment_dates=true&per_page=50"









#  make sure to get the current time zone of the parse inorder
#  to change the time in the future

