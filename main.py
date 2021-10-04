from flask import Flask, app, render_template
import csv

app = Flask(__name__)

@app.route("/")
def index():
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

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)