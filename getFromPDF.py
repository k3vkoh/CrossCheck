import pdfplumber
import json

syllabus = "theatre.pdf"

def extract(syllabus):

	with pdfplumber.open(syllabus) as pdf:

		# # this methods extracts text that is not a table in extract_table() 
		# for x in range(len(pdf.pages)):
		# 	temp_page = pdf.pages[x]
		# 	info = temp_page.extract_table()
		# 	calendar_list = []
		# 	if info != None:
		# 		print(type(info))
		# 		print(info)
		# 		calendar_list.append(info)
		# 		print('')
		# 		print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
		# 		print('')


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
			if "/" in text_list[i]:
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
						if "/" in temp[j]:
							temp_list.append(temp[j])
							dateTrue = False
					else:
						word += temp[j] + " "
					j += 1
				temp_list.append(word)
				# for x in temp:
				# 	if x not in ignore
				calendar_list.append(temp_list)
			i += 1



		# one way to approach using while True
		# i = 0
		# while i < len(text_list):
		# 	if "calendar" in text_list[i]:
				
		# 		#  this need to utilize regular expressions 
		# 		while True:
		# 			if "/" not in text_list[i]:
		# 				# if no / then no date supposedly
		# 				i += 1
		# 			else:
		# 				# if there is a / then need to check if it follows the regex {num}/{num}
		# 				temp = text_list[i]
		# 			print(temp)
		# 			i += 1
		# 			if temp == " ":
		# 				break
		# 			calendar_list.append(temp)
		# 	i += 1


		# print(calendar_list)


		with open('calendar.json', 'w') as json_file:
			# json.dump(text_list, json_file, indent = 1)
			json.dump(calendar_list, json_file, indent = 1)

		print("done")


# extract(syllabus)

