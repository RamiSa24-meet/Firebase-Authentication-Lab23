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
  "databaseURL":"https://ramiproject-1e8b8-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


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
        except Exception as e:
            print(e)
            return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  
  
  if request.method == 'GET':
    return render_template('signup.html')
  else:
    try:
      user = {"email":request.form['email'],"fullname":request.form['fullname'] ,"username":request.form['username'],"bio":request.form['bio']}
      print(user)
      z =request.form['email'] 
      x = request.form['password']
      login_session['user']= auth.create_user_with_email_and_password(z,x)
      uid = login_session['user']['localId']
      db.child("users").child(uid).set(user)
      return render_template('add_tweet.html')
    except Exception as e :
        print(e)
        return render_template("signup.html")
    

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    
    if request.method == 'GET':
        return redirect(url_for('add_tweet'))
    else:
        try:
            tweet= {"title":request.form["title"],"text":request.form["text"],"uid":login_session['user']["localId"]}
            db.child("tweets").push(tweet)
            print(tweet)
            return redirect(url_for('all_tweets'))
        except:
            return redirect('add_tweet.html')



@app.route('/alltweets', methods=['GET', 'POST'])
def all_tweets():
   print("wdawdawdaw")
   print(db.child("tweets").get().val())
   return render_template('alltweets.html',data = db.child("tweets").get().val())



if __name__ == '__main__':
    app.run(debug=True)