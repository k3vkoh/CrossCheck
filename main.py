import getFromPDF
import getFromAPI
import toDB

# syllabus = "theatre.pdf"
# syllabus = "pulse.pdf"
syllabus = "lit core.pdf"
my_courses = [1630778, 1631956, 1628579, 1631190]
# my_courses = [1628579]

def main():
	# print("main")
	# getFromPDF.extract(syllabus)
	for course in my_courses:
		data = getFromAPI.extract(course)
		toDB.add_to_db(data)

		# with open('data.json', 'w') as json_file:
		# 	json.dump(final_sch, json_file, indent = 1)
		# 	json.dump(r.json(), json_file, indent = 1)

if __name__ == "__main__":
	main()
# print('hello')
# main()