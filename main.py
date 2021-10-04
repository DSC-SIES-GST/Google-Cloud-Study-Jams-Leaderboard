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
                    "track1": row[1],
                    "track2": row[2],
                    "tracktotal": int(row[1]) + int(row[2])
                })
            else:
                first_line = False
    leaderboard.sort(key=lambda x: x['tracktotal'], reverse=True)
    return render_template("index.html", leaderboard=leaderboard)

if __name__ == "__main__":
    app.run(debug=True)