import pandas as pd
import pyrebase

# Configure Firebase project
config = {
  "apiKey": "REPLACE_WITH_ORIGINAL_VALUE",
  "authDomain": "REPLACE_WITH_ORIGINAL_VALUE",
  "databaseURL": "REPLACE_WITH_ORIGINAL_VALUE",
  "projectId": "REPLACE_WITH_ORIGINAL_VALUE",
  "storageBucket": "REPLACE_WITH_ORIGINAL_VALUE",
  "messagingSenderId": "REPLACE_WITH_ORIGINAL_VALUE",
  "appId": "REPLACE_WITH_ORIGINAL_VALUE",
  "measurementId": "REPLACE_WITH_ORIGINAL_VALUE"
}
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
