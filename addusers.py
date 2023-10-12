import pandas as pd
import pyrebase
import os

from dotenv import load_dotenv

load_dotenv()
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
# print(config)
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

try:
    # Read csv file
    df = pd.read_csv('student_authentication.csv')
    # Get the data from the csv file
    data = df.values.tolist()
    # Loop through the data
    for user in data:
        # Create a new user
        auth.create_user_with_email_and_password(user[0], user[1])
        print('User created: ' + user[0])
except Exception as e:
    print(e)
