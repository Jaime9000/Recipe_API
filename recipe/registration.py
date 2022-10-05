#!/bin/python

from flask import Flask, render_template,request,redirect,url_for,session,logging

app = Flask(__name__)


users = {}

class Register:
    '''Registration Form'''
    def __init__(self,app):
        self.app = app
    def signup(self,username,password):
        p = hash(password)
        users.update({username:p}) 
    def login(self,username,password):
        p=hash(password)
        if users[username] == p:
            return "Successfully loggeed-in"
        else:
            return "Wrong Username/Password"
u1 = Register('Obj_1')
u1.signup('jimmyschermer','slotshot26')
u2 = Register('Obj_2')
u2.signup('puyoljohnson','Slot26')

#print(dir(Register))
#print(users)
#print(u1.login('jimmyschermer','slotshot26'))
#print(u1.login('jimmyschermer','slotshot\6'))

userObject = Register(app)

@app.route('/')
def home():
    return render_template("/home.html")
   # return '''<h>this is demo flask app</h>
   # <p> for signup - /signup/username/password </p>
   # <p> for login - /login/username/password </p>'''

#@app.route('/signup/<username>/<password>')
#def signup(username,password):
 #   userObject.signup(username,password)
  #  return f'''<marguee> {username} has been successfully registered <marquee>'''
#@app.route('/login/<username>/<password>')
#def login(username,password):
#    auth = userObject.login(username,password)
#    if auth:
#        return f'''<p> {username} logged in successfully <p>'''
#    else:
#        return f'''<p> {username} username and password donot match, please renter you username/password <p>'''
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST': 
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        return '{} is successfully registered'.format(username)
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        print(users)
        try:
            if users['username'] == password:
                return '{} , you have successfully logged in'.format(username)
            else:
                return 'Incorrect password, please retype password and submit again'
        except:
            return 'Wrong Password'
    return render_template('login.html')
@app.route('/user/data')
def user_data():
    return users
