from flask import Flask, app, render_template, request, session, url_for, redirect
from datetime import timedelta
import csv
import pyrebase

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=1)
app.secret_key = ''

config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": "",
  "measurementId": ""
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route("/")
def index():
    if "uname" in session:
        with open('mycsv.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            first_line = True
            leaderboard = []
            for row in data:
                if not first_line:
                    leaderboard.append({
                        "name": row[0],
                        "tracktotal": int(row[1])
                    })
                else:
                    first_line = False
        leaderboard.sort(key=lambda x: x['tracktotal'], reverse=True)
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