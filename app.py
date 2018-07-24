from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('homepage.html')
    else:
        username = session["user"]
        reminder = session['reminder']
        return render_template('after_sign_in.html',username=username, reminder=reminder )
@app.route('/sign_in')
def signIn():
    session['logged_in'] = False
    return render_template('login.html')

@app.route('/calendar')
def calendar():
    session['logged_in'] = True
    return render_template('calendar.html')

@app.route('/sign_up')
def signUp():
    session['logged_in'] = False
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    usersFile = open("users.json", "r")
    users = json.load(usersFile)
    usersFile.close()

    if users[POST_USERNAME]["pass"]==POST_PASSWORD:
        session["user"] = POST_USERNAME;
#UPDATE REMINDERS
        session['reminder'] = users[POST_USERNAME]['reminder']
        '''
        session['planet'] = users[POST_USERNAME]['planet']
        '''
        session['logged_in'] = True
    else:
        flash('wrong password!')
        return home()
    return home()




@app.route('/register', methods=['POST'])

def register():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    usersFile = open("users.json", "r")
    users = json.load(usersFile)
    usersFile.close()
    if POST_USERNAME in users:
        flash("This username already exists!")

    else:
        users[POST_USERNAME]={"pass":POST_PASSWORD, "reminder":[]}

        usersFile = open('users.json', 'w')
        json.dump(users, usersFile) #json.dump(data, nameoffile)
        usersFile.close()
    return home()

@app.route('/add_reminder', methods=['POST'])

def add_reminder():
    POST_REMINDER_DATE = str(request.form['reminder_date'])
    POST_REMINDER_TITLE = str(request.form['reminder_title'])
    usersFile = open("users.json", "r")
    users = json.load(usersFile)
    usersFile.close()

    users[session["user"]]["reminder"].append({"date":POST_REMINDER_DATE, "title":POST_REMINDER_TITLE})
    usersFile = open("users.json", "w")
    json.dump(users, usersFile) #json.dump(data, nameoffile)
    usersFile.close()
    session["reminder"] = users[session["user"]]["reminder"]
    return home()





@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
