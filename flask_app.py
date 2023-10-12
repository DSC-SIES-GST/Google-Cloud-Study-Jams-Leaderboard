from flask import Flask, app, render_template, request, session, url_for, redirect
from datetime import timedelta
import pyrebase
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=1)

# Set a secret key for your application
app.secret_key = os.environ.get('SECRET_KEY')

# Configure Firebase project
config = {
  "apiKey": os.getenv('API_KEY'),
  "authDomain": os.environ.get('AUTH_DOMAIN'),
  "databaseURL": os.environ.get('DATABASE_URL'),
  "projectId": os.environ.get('PROJECT_ID'),
  "storageBucket": os.environ.get('STORAGE_BUCKET'),
  "messagingSenderId": os.environ.get('MESSAGING_SENDER_ID'),
  "appId": os.environ.get('APP_ID'),
  "measurementId": os.environ.get('MEASUREMENT_ID')
}
print(config)
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    if "uname" in session:
        my_csv = os.path.join(THIS_FOLDER, 'leaderboard.csv')
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
        return render_template("index.html")

@app.route('/logout')
def logout():
    session.pop('uname', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = True
    app.run()