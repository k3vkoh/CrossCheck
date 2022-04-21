import requests 
import json
from datetime import datetime, timezone

token = "1019~wYCvNSHeAkCg9Va6rQDTFipPKzzTtAECooM6G8msOUL8fhM2yrACqfYzP0WRo8TG"

headers = {"Authorization" : "Bearer {}".format(token)}
params = {"state[]" : "all"}

my_courses = [1630778, 1631956, 1628579, 1631190]

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def day_of_the_week(dayNum):
	if dayNum == 0:
		return "Monday"
	if dayNum ==  1:
		return "Tuesday"
	if dayNum ==  2:
		return "Wednesday"
	if dayNum ==  3:
		return "Thursday"
	if dayNum ==  4:
		return "Friday"
	if dayNum ==  5:
		return "Saturday"
	if dayNum ==  6:
		return "Sunday"

def extract(course):
	final_sch = {"course": [] ,"name" : [], "due_date": [], "due_time": [], "day_name": [], "method": [], "submission_status": []}

	url = "https://bostoncollege.instructure.com/api/v1/courses/{}/assignment_groups?exclude_assignment_submission_types%5B%5D=wiki_page&exclude_response_fields%5B%5D=description&exclude_response_fields%5B%5D=rubric&include%5B%5D=assignments&include%5B%5D=discussion_topic&override_assignment_dates=true&per_page=50".format(str(course))

	r = requests.get(url, headers = headers, params = params)

	assignment_groups = r.json()
	for group in assignment_groups:
		for assignment in group["assignments"]:
			assignment_name = assignment["name"]
			date_temp = assignment["due_at"]
			submission_status = str(assignment["has_submitted_submissions"])
			try:
				date_temp = date_temp.strip("Z")
				date_temp = date_temp.replace("T", " ")
				date_temp = date_temp.replace("-", "/")
				date_time_obj = datetime.strptime(date_temp, '%Y/%m/%d %H:%M:%S')
				date_time_local = utc_to_local(date_time_obj)
				local_due_string = date_time_local.strftime('%Y-%m-%d %H:%M:%S')
				date_split = local_due_string.split()
				due_date = date_split[0]
				due_time = date_split[1]
				day_name = day_of_the_week(date_time_local.weekday())
			except: 
				due_date = ""
				due_time = ""
				day_name = ""
			final_sch["course"].append(course)
			final_sch["name"].append(assignment_name)
			final_sch["due_date"].append(due_date)
			final_sch["due_time"].append(due_time)
			final_sch["day_name"].append(day_name)
			final_sch["method"].append("api")
			final_sch["submission_status"].append(submission_status)
	print(r)

	# with open('data.json', 'w') as json_file:
	# 		json.dump(final_sch, json_file, indent = 1)
			# json.dump(r.json(), json_file, indent = 1)

	return final_sch









# url = "https://bostoncollege.instructure.com/api/v1/courses/1631325/assignment_groups?exclude_assignment_submission_types%5B%5D=wiki_page&exclude_response_fields%5B%5D=description&exclude_response_fields%5B%5D=rubric&include%5B%5D=assignments&include%5B%5D=discussion_topic&override_assignment_dates=true&per_page=50"









#  make sure to get the current time zone of the parse inorder
#  to change the time in the future

