import pdfplumber
import json
import re

syllabus = "theatre.pdf"

def extract(syllabus):

	with pdfplumber.open(syllabus) as pdf:


		file_text = ""
		# this methods will just iterated through every line 
		for x in range(len(pdf.pages)):
			file_text += pdf.pages[x].extract_text() + "\n"
		
		file_text = file_text.lower()
		# print(file_text)
		text_list = file_text.split("\n")
		# print(text_list)

		# list of lists whose items are date and assignment
		calendar_list = []


		# use regex in the if after the first while and no while true

		i = 0
		while i < len(text_list):
			pattern = "([0-1][0-9][/][0-9][0-9]|[0-1][0-9][/][0-9]|[0-9][/][0-9][0-9]|[0-9][/][0-9])"
			if re.search(pattern, text_list[i]):
				print(text_list[i])
				# ignore = ["m", "t", "w", "th", "f", "mon", "tue", "wedn", "thurs", "fri"]
				temp = text_list[i].split()
				temp_list = []
				word = ""
				dateTrue = True
				j = 0
				while j < len(temp):
					if dateTrue:
						# also regex for date
						# convert date to type date 
						if re.match(pattern, temp[j]):
							temp_list.append(temp[j])
							dateTrue = False
					else:
						word += temp[j] + " "
					j += 1
				temp_list.append(word)
				# for x in temp:
				# 	if x not in ignore
				if temp_list != [""]:
					calendar_list.append(temp_list)
			i += 1

		# print(calendar_list)

		with open('calendar.json', 'w') as json_file:
			# json.dump(text_list, json_file, indent = 1)
			json.dump(calendar_list, json_file, indent = 1)

		print("done")


# extract(syllabus)

