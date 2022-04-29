import pandas as pd 
from sqlalchemy.types import Text
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import webbrowser
import pyautogui
import pyperclip
import time
import datetime

import getFromAPI

engine = create_engine('sqlite:////Users/kevinkoh/Desktop/CrossCheck/cc.db')

def get_token(canvas_username, canvas_password):

	url = 'https://bostoncollege.instructure.com/profile/settings'

	driver = webdriver.Chrome('./chromedriver')
	driver.maximize_window()
	driver.get(url)

	username = driver.find_element_by_xpath('//*[@id="username"]')
	username.send_keys(canvas_username)

	password = driver.find_element_by_xpath('//*[@id="password"]')
	password.send_keys(canvas_password)

	submit = driver.find_element_by_xpath('/html/body/section/form/button')
	submit.send_keys(Keys.RETURN)

	access = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[3]/div[2]/a')
	access.send_keys(Keys.RETURN)

	token_purpose = driver.find_element_by_xpath('//*[@id="access_token_purpose"]')
	token_purpose.send_keys("CrossCheck")

	generate = driver.find_element_by_xpath('/html/body/div[5]/div[4]/div/button[2]')
	generate.send_keys(Keys.RETURN)

	# pyautogui.moveTo(500, 427)
	# time.sleep(2) 
	# pyautogui.click()
	# time.sleep(2) 
	# pyautogui.click(clicks = 3, interval=0.25)
	# interval=0.25
	# pyautogui.hotkey('command', 'c')
	# time.sleep(2) 

	pyautogui.moveTo(473, 427)
	time.sleep(2)
	pyautogui.dragTo(1070, 425, button = 'left')
	time.sleep(2) 
	pyautogui.hotkey('command', 'c')
	time.sleep(1)  
	driver.close()
	token = pyperclip.paste()
	tok_list = token.split('\n')
	print(tok_list)
	final_token = tok_list[0]
	return final_token


# undo 
	# time.sleep(10)

	# driver.close()

def signup(email, password, canvas_us, canvas_pw, token):

	try:
		df = pd.DataFrame({"email": [email], "password": [password], "canvas_username": [canvas_us], "canvas_password": [canvas_pw], "token": [token]})
		df.to_sql('user', engine, if_exists = 'append', index = False)
		print("done")
		return True
	except: 
		return False

# def add_token(token, username, password):
	
# 	sql = """
# 			UPDATE user
# 			SET token = '{}'
# 			WHERE email = '{}' and password = '{}'
# 	""".format(token, username, password)

	# sql = """
	# 		SELECT * FROM user 
	# 		WHERE email = '{}' and password = '{}'
	# 	""".format(username, password)
		
	# df = pd.read_sql(sql, engine)

	# sql = """ 
	# 	DELETE FROM user
	# 	WHERE email = '{}' and password = '{}'
	# """.format(username, password)
	# with engine.begin() as connection:
	# 	try:
	# 		print('deleted user')
	# 		connection.execute(sql)
	# 	except:
	# 		print('failed to delete user')

	# df['token'][0] = token
	# df.to_sql('user', engine, if_exists = 'append', index = False)
	# print("done")




def set_up(email, course_name, course_num):
	df = pd.DataFrame({"email": [email], "course_name": [course_name], "course_num": [course_num]})
	df.to_sql('user_classes', engine, if_exists = 'append', index = False)
	print("done")
	return True

def login(username, password):

	sql = """
			SELECT * FROM user 
			WHERE email = '{}' and password = '{}'
		""".format(username, password)
	df = pd.read_sql(sql, engine)

	try:
		if df["email"][0] == username and df["password"][0] == password:
			print("login success")
			return True
	except:
		print("login failed")
		return False


# this function is only used in getFromAPI.py
def add_schedule(schedule):
	df = pd.DataFrame(schedule)
	df.to_sql('assignments', engine, if_exists = 'append', index = False)
	print("done")

def get_classes(email):
	sql = """
			SELECT course_num FROM user_classes 
			WHERE email = '{}'
		""".format(email)
	df = pd.read_sql(sql, engine)

	return df

def get_class(email, course_num):
	sql = """
			SELECT course_name FROM user_classes 
			WHERE email = '{}' and course_num = '{}'
		""".format(email, course_num)
	df = pd.read_sql(sql, engine)

	return df["course_name"][0]

def get_token_db(email):
	sql = """
			SELECT token FROM user 
			WHERE email = '{}'
		""".format(email)
	df = pd.read_sql(sql, engine)

	return df['token'][0]

def make_schedule(email, token):
	df = get_classes(email)

	for course in df['course_num']:
		getFromAPI.extract(email, token, course)

def update_schedule(email, token):
	sql = """ 
			DELETE FROM assignments
			WHERE email = '{}' and method = 'api'
		""".format(email)
	with engine.begin() as connection:
		try:
			connection.execute(sql)
			print('done')
		except:
			pass

	df = get_classes(email)

	for course in df['course_num']:
		getFromAPI.extract(email, token, course)


def schedule_to_json(email):
	sql = """
			SELECT * FROM assignments 
			WHERE email = '{}'
		""".format(email)
	df = pd.read_sql(sql, engine)
	file = df.to_json(index = False, orient = 'table', indent = 1)
	return file


def add_assignment(email, course_num, assignment_name, due_date, due_time, day_name, method, submission_status):
	schedule = {"email" : [],"course_num": [] ,"course_name": [], "assignment_name" : [], "due_date": [], "due_time": [], "day_name": [], "method": [], "submission_status": []}
	df = pd.DataFrame(schedule)
	df.to_sql('assignments', engine, if_exists = 'replace', index = False)
	print("done")

def clear_all():
	sql = """ 
			DELETE FROM assignments
		"""
	with engine.begin() as connection:
		try:
			print('deleted assignments')
			connection.execute(sql)
		except:
			print('failed to delete assignments')

	sql = """ 
			DELETE FROM user_classes
		"""
	with engine.begin() as connection:
		try:
			print('deleted user_classes')
			connection.execute(sql)
		except:
			print('failed to delete user_classes')

	sql = """ 
			DELETE FROM user
		"""
	with engine.begin() as connection:
		try:
			print('deleted user')
			connection.execute(sql)
		except:
			print('failed to delete user')

	print("cleared all")

def reset():
	schedule = {"email" : [],"course_num": [] ,"course_name": [], "assignment_name" : [], "due_date": [], "due_time": [], "day_name": [], "method": [], "submission_status": []}
	df = pd.DataFrame(schedule)
	df.to_sql('assignments', engine, if_exists = 'replace', index = False, dtype = Text)
	print("done")


if __name__ == "__main__":
	canvas_username = 'kohke'
	canvas_password = 'Green1Card'
	# email = "hello@gmail.com"

	# step 1, get token for sign up
	# print(get_token(canvas_username, canvas_password))

	# step 2, save token
	# token = "1019~ltKPMCXVcYR4iWgqIol2uw5JtLE7x0VuYFwJDTAwT1kH4u11HoCsIDXL9WoPhKgB"
	# signup("hello@gmail.com", "password", canvas_username, canvas_password, token)
	
	#step 2.5, check login
	# print(login("hello@gmail.com", "password"))

	# step 3, save classes
	# set_up(email, "PULSE", "1630778") 
	# set_up(email, "PROBABILITY", "1631956")
	# set_up(email, "SWIFT", "1628579")
	# set_up(email, "GLOB 2", "1631190")

	#step4, get schedule
	# make_schedule(email, token)
	# schedule_to_json(email)


	#step 5, get update
	# update_schedule(email, token)
	# schedule_to_json(email)

	# last step for demonstration
	# clear_all()

	reset()

	# print(get_token_db('kohke@bc.edu'))












