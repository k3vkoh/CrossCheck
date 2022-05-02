from flask import Flask, redirect, url_for, render_template, request
import toDB
import json


app = Flask(__name__)

username = ""
password = ""
canvas_username = ""
canvas_password = ""
token = ""
json_file = None

@app.route("/")
def home():
    return render_template('home.html') 

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')

@app.route('/setup', methods=['POST', 'GET'])
def setup():
    print(request.get_data())

    global email, password, canvas_username, canvas_password, token
    email = request.form.get('username')
    password = request.form.get('password')
    canvas_username = request.form.get('canvas_username')
    canvas_password = request.form.get('canvas_password')
    token = toDB.get_token(canvas_username, canvas_password)

    toDB.signup(email, password, canvas_username, canvas_password, token)
    return render_template('setup.html')

# add error message
@app.route('/setup_repeat', methods=['POST', 'GET'])
def setup_repeat():
    print(request.get_data())

    if request.form.get('course_num') != None and request.form.get('course_num') != "":
        course_num = request.form.get('course_num')
        course_name = request.form.get('course_name')
        toDB.set_up(email, course_name, course_num)

    return render_template('setup_repeat.html')

@app.route('/schedule_su', methods=['POST', 'GET'])
def schedule_su():
    
    global json_file
    toDB.make_schedule(email, token)
    json_file = toDB.schedule_to_json(email)
    return render_template("schedule_su.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/schedule', methods=['POST', 'GET'])
def schedule():
    print(request.get_data())

    global json_file
    email_local = request.form.get('username')
    password_local = request.form.get('password')

    if toDB.login(email_local, password_local):
        token_local = toDB.get_token_db(email_local)
        toDB.update_schedule(email_local, token_local)
        json_file = toDB.schedule_to_json(email_local)
        return render_template("schedule.html")
    else: 
        return render_template("login.html")
    return render_template("schedule.html")

@app.route('/show_schedule', methods=['POST', 'GET'])
def show_schedule():
    
    global json_file
    return json_file


# for api call via app

@app.route('/login_db/<username_local>/<password_local>')
def login_db(username_local, password_local):
    return toDB.get_success(toDB.login(username_local, password_local))



@app.route('/get_schedule/<username_local>/<password_local>')
def get_schedule(username_local, password_local):
    if toDB.login(username_local, password_local):
        token_local = toDB.get_token_db(username_local)
        toDB.update_schedule(username_local, token_local)
        return toDB.schedule_to_json(username_local)

    else:
        return "Parsing Failed"


@app.route('/signup_db/<username_local>/<password_local>/<canvas_username_local>/<canvas_password_local>', methods=['POST', 'GET'])
def signup_db(username_local, password_local, canvas_username_local, canvas_password_local):
    print("signup_db")
    try:
        token_local = toDB.get_token(canvas_username_local, canvas_password_local)
        toDB.signup(username_local, password_local, canvas_username_local, canvas_password_local, token_local)
        return toDB.get_success(True)
    except:
        return toDB.get_success(False)

@app.route('/setup_db/<username_local>/<course_string>', methods=['POST', 'GET'])
def setup_db(username_local, course_string):
    try:
        temp = course_string.split(',')
        for x in temp:
            temp_split = x.split(':')
            course_name = temp_split[0].replace("_", " ")
            toDB.set_up(username_local, course_name, temp_split[1])
        return toDB.get_success(True)
    except:
        return toDB.get_success(False)

@app.route('/add_course_db/<username_local>/<course_name>/<course_num>', methods=['POST', 'GET'])
def add_course_db(username_local, course_name, course_num):
    try:
        temp_name = course_name.replace("_", " ")
        toDB.set_up(username_local, temp_name, course_num)
        return toDB.get_success(True)
    except:
        return toDB.get_success(False)

@app.route('/add_assignment_db/<username_local>/<course_name>/<course_num>/<assignment_name>/<due_date>/<due_time>/<day_name>', methods=['POST', 'GET'])
def add_assignment_db(username_local, course_name, course_num, assignment_name, due_date, due_time, day_name):
    try:
        temp_name = course_name.replace("_", " ")
        temp_assignment = assignment_name.replace("_", " ")
        toDB.add_assignment(username_local, temp_name, course_name, temp_assignment, due_date, due_time, day_name, 'user', 'false')
        return toDB.get_success(True)
    except:
        return toDB.get_success(False)

if __name__ == "__main__":
    # app.run(ssl_context='adhoc')
    app.run()
