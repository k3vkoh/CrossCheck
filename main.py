import getFromPDF
import getFromAPI

# syllabus = "theatre.pdf"
syllabus = "pulse.pdf"

def main():
	# print("main")
	getFromPDF.extract(syllabus)

if __name__ == "__main__":
	main()
# print('hello')
# main()