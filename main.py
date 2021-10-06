from flask import Flask, app, render_template, request, session, url_for, redirect
from datetime import timedelta
import pyrebase
import pandas as pd
import os

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=1)
app.secret_key = 'dscsiesgst30daysofgooglecloud'

config = {
  "apiKey": "AIzaSyDz4k82KSOGZAM6xdoOA7DZ9FMGkj5Q2UI",
  "authDomain": "daysofcloud-d8428.firebaseapp.com",
  "databaseURL": "https://daysofcloud-d8428-default-rtdb.firebaseio.com",
  "projectId": "daysofcloud-d8428",
  "storageBucket": "daysofcloud-d8428.appspot.com",
  "messagingSenderId": "824714996975",
  "appId": "1:824714996975:web:402f8e0198bc0f3423ff1a",
  "measurementId": "G-GXWZPTPQDG"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    if "uname" in session:
        my_csv = os.path.join(THIS_FOLDER, 'mycsv.csv')
        leaderboard = pd.read_csv(my_csv)
        leaderboard = leaderboard.sort_values(by=['Total'], ascending=False)
        leaderboard = leaderboard.values.tolist()
        return render_template("index.html", leaderboard=leaderboard)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['POST','GET'])
def login():
    if "uname" in session:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                session.permanent = True
                session['uname'] = email
                return redirect(url_for('index'))
            except:
                return render_template("login.html", unsuccesful="Invalid Credentials")
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('uname', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()