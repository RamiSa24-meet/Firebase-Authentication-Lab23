from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyBvzOLi6PTd4-GtXEL6w_q9ea2cmFoVJF4",
  "authDomain": "ramiproject-1e8b8.firebaseapp.com",
  "projectId": "ramiproject-1e8b8",
  "storageBucket": "ramiproject-1e8b8.appspot.com",
  "messagingSenderId": "200153313749",
  "appId": "1:200153313749:web:638242bcaa8eab4a818d5c",
  "measurementId": "G-9WRT1JPEG0",
  "databaseURL":"https://console.firebase.google.com/project/ramiproject-1e8b8/database/ramiproject-1e8b8-default-rtdb/data/~2F"
};
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()








app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == "GET":
      return render_template("signin.html")
    else:
        try:
            z =request.form['email'] 
            x = request.form['password']
            auth.sign_in_with_email_and_password(z,x)
            return render_template("add_tweet.html")
        except :
            render_template("signin.html")
        return "there was an erorr"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  user = {"email":request.form['email'],"password":request.form['password'],"fullname":request.form['fullname'] ,"username":request.form['username'],"bio":request.form['bio']}
  uid = login_session['user']['localId']
  if request.method == 'GET':
    return render_template('signup.html')
  else:
    try:
      z =request.form['email'] 
      x = request.form['password']
      login_session['user']= auth.create_user_with_email_and_password(z,x)
      return render_template('add_tweet.html')
    except:
        return render_template("add_tweet.html")
    return "there was an erorr"

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)