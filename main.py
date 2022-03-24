import getFromPDF
import getFromAPI

# syllabus = "theatre.pdf"
syllabus = "pulse.pdf"
my_courses = [1630778, 1631956, 1628579, 1631190]

def main():
	# print("main")
	getFromPDF.extract(syllabus)
	# getFromAPI.extract(my_courses)

if __name__ == "__main__":
	main()
# print('hello')
# main()