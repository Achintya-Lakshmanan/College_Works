# Import libraries
from flask import Flask, render_template, request, session, redirect
import pyodbc
import pandas as pd
import torch
from model import ANN

# Create a flask app
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'achintya'

# Load the model and other objects
model = ANN()
model = torch.load('model.pth') # Load the model
encoder1 = torch.load('encoder1.pkl') # Load the encoder
encoder2 = torch.load('encoder2.pkl') # Load the encoder
encoder3 = torch.load('encoder3.pkl') # Load the encoder
encoder4 = torch.load('encoder4.pkl') # Load the encoder
encoder5 = torch.load('encoder5.pkl') # Load the encoder

# Define a route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    # If the request method is GET, render the login.html template
    if request.method == "GET":
        return render_template("login.html")
    # If the request method is POST, get the username and password from the form
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Connect to ms sql database using pyodbc
        conn = pyodbc.connect("Driver={SQL Server};"
                              "Server=DESKTOP-GM0CKCM\SQLEXPRESS;"
                              "Database=CIA_2;"
                              "Trusted_Connection=yes")
        # Create a cursor object
        cursor = conn.cursor()
        # Execute a query to check if the username and password are valid
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        # Fetch one row from the result
        row = cursor.fetchone()
        # Close the connection
        conn.close()
        # If the row is not None, it means the login is successful
        if row is not None:
            # Redirect to the input page
            session['username'] = username
            return redirect("/input")
        # If the row is None, it means the login is failed
        else:
            # Render the login.html template with an error message
            return render_template("login.html", error="Invalid username or password")
        
# Define a route for input page
@app.route('/input', methods=['GET', 'POST'])
def input():
    # Check if the user is logged in
    if 'username' in session:
        # Check if the request method is POST
        if request.method == 'POST':
            # Get the values for the features from the form
            gender = request.form['gender']
            race_ethnicity = request.form['race/ethnicity']
            parental_level_of_education = request.form['parental level of education']
            lunch = request.form['lunch']
            test_preparation_course = request.form['test preparation course']
            
            # Create a dataframe with the features
            df = pd.DataFrame([[gender, race_ethnicity, parental_level_of_education, lunch, test_preparation_course]], columns=['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course'])
            
            # Encode the categorical features using the encoder object
            df["gender"] = encoder1.transform(df["gender"])
            df["race/ethnicity"] = encoder2.transform(df["race/ethnicity"])
            df["parental level of education"] = encoder3.transform(df["parental level of education"])
            df["lunch"] = encoder4.transform(df["lunch"])
            df["test preparation course"] = encoder5.transform(df["test preparation course"])

            display(df)
            # Convert the dataframe to a tensor
            df = df.values
            df = torch.from_numpy(df).float()
            print(df)
            # Predict the scores using the model object
            scores = model(df)
            
            # Detach and round the scores to integers
            scores = scores.detach().numpy().round(2)
            
            # Extract the math score, reading score, and writing score from the scores array
            math_score = scores[0][0]
            reading_score = scores[0][1]
            writing_score = scores[0][2]
            
            # Render the output page template with the predicted scores
            return render_template('output.html', math_score=math_score, reading_score=reading_score, writing_score=writing_score)
        # If the request method is not POST, render the input page template
        else:
            return render_template('input.html')
    # If the user is not logged in, redirect to the login page
    else:
        return redirect('/')