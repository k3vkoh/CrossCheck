from flask import Flask, redirect, url_for, render_template, request
import toDB


app = Flask(__name__)

username = ""
password = ""
canvas_username = ""
canvas_password = ""
token = ""

@app.route("/")
def home():
    return render_template('home.html') 

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')

@app.route('/call_get_token', methods=['POST', 'GET'])
def call_get_token():

    print(request.get_data())

    global email, password, canvas_username, canvas_password
    email = request.form.get('username')
    password = request.form.get('password')
    canvas_username = request.form.get('canvas_username')
    canvas_password = request.form.get('canvas_password')

    print(email)
    print(password)
    print(canvas_username)
    print(canvas_password)

    toDB.get_token(canvas_username, canvas_password)

    return render_template('call_to_get_token.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/setup', methods=['POST', 'GET'])
def setup():
    print(request.get_data())

    global token
    token = request.form.get('token')
    toDB.signup(email, password, canvas_username, canvas_password, token)
    return render_template('setup.html')

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
    
    toDB.make_schedule(email, token)
    json_file = toDB.schedule_to_json(email)
    print("hello")
    print(json_file)
    print("hello")
    return json_file

@app.route('/schedule', methods=['POST', 'GET'])
def schedule():
    print(request.get_data())

    global email, password
    email = request.form.get('username')
    password = request.form.get('password')

    toDB.update_schedule(email, token)
    json_file = toDB.schedule_to_json(email)
    print(json_file)
    return json_file

if __name__ == "__main__":
    app.run()

