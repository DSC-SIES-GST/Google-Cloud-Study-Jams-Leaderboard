import pandas as pd
import pyrebase

# Configure Firebase project
config = {
  "apiKey": "AIzaSyAlhjvfQDcwuCziQGhwAp2qwGrcNAZCSLM",
  "authDomain": "daysofcloud-292c2.firebaseapp.com",
  "databaseURL": "https://daysofcloud-292c2-default-rtdb.firebaseio.com",
  "projectId": "daysofcloud-292c2",
  "storageBucket": "daysofcloud-292c2.appspot.com",
  "messagingSenderId": "701838918926",
  "appId": "1:701838918926:web:ea5c74dd5ad83d3eac035f",
  "measurementId": "G-WXYF79XWP4"
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