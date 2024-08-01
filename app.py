"""
### Overview
`app.py` is the main script that runs the Flask web application for the Weather App. It handles routing, user authentication, and fetching weather data.

### Structure

1. **Imports**
   ```python
   from flask import Flask, render_template, request, redirect, url_for, session
   import requests
   ```
   - `Flask`: Framework for creating the web application.
   - `render_template`: Renders HTML templates.
   - `request`, `redirect`, `url_for`, `session`: Handles HTTP requests, redirects, URL building, and session management.
   - `requests`: Makes HTTP requests to external APIs.

2. **App Configuration**
   ```python
   app = Flask(__name__)
   app.secret_key = 'your_secret_key'
   ```
   - Initializes the Flask application and sets a secret key for session management.

3. **Routes**
   - **Home Route**
     ```python
     @app.route('/')
     def home():
         return render_template('home.html')
     ```
     Renders the home page.

   - **Signup Route**
     ```python
     @app.route('/signup', methods=['GET', 'POST'])
     def signup():
         if request.method == 'POST':
             # Handle signup logic
         return render_template('signup.html')
     ```
     Handles user signup with both GET and POST methods.

   - **Login Route**
     ```python
     @app.route('/login', methods=['GET', 'POST'])
     def login():
         if request.method == 'POST':
             # Handle login logic
         return render_template('login.html')
     ```
     Handles user login with both GET and POST methods.

   - **Logout Route**
     ```python
     @app.route('/logout')
     def logout():
         session.pop('user', None)
         return redirect(url_for('home'))
     ```
     Logs out the user by clearing the session.

   - **Weather Route**
     ```python
     @app.route('/weather', methods=['GET', 'POST'])
     def weather():
         if 'user' in session:
             if request.method == 'POST':
                 city = request.form['city']
                 # Fetch weather data
             return render_template('weather.html')
         return redirect(url_for('login'))
     ```
     Displays weather information. If the user is not logged in, it redirects to the login page.

4. **Running the App**
   ```python
   if __name__ == '__main__':
       app.run(debug=True)
   ```
   Starts the Flask application in debug mode.

### Explanation
- **Routing**: Defines endpoints for different pages like home, signup, login, logout, and weather.
- **User Authentication**: Uses sessions to manage user login state.
- **Weather Data**: Fetches weather information based on user input (city) using the `requests` module.

This script ties together the backend functionality of the weather application, ensuring users can sign up, log in, view weather information, and log out.
"""


from flask import Flask, render_template,request
import requests 
import json
import datetime
import pymysql as sql

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/wether",methods=["post","get"])
def wether():
    city=request.form.get("city")

    api_key = "ccf7bd0fcf6e7edb60a2cbfbe595a045"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    resp = requests.get(url)
    print(resp)
    data = resp.json()
    if resp.status_code ==200:
        city_name = data["name"]
        temp = data["main"]["temp"]
        min_temp = data['main']['temp_min']
        max_temp = data['main']['temp_max']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wether={"city_name":city_name,"temp":temp,"pressure":pressure,"humidity":humidity}
        print(wether)
        now = datetime.datetime.now()

        # Format the date and day
        date = now.strftime("%Y-%m-%d")  # Format: Year-Month-Day
        day = now.strftime("%A")  # Full weekday name

        # Print the date and day
        print("Date:", date)
        print("Day:", day)

        return render_template("wether.html",wether=wether,date=date,day=day ,city=city)
    else:
        return "data not found"

@app.route("/afterlogin",methods=["POST","GET"])
def afterlogin():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        print(email)
        print(password)
        connect =sql.connect(host="localhost",port=3306,user="root",password="",database="weather_app")
        cur=connect.cursor()
        cur.execute("select * from signup where email=%s and password =%s",(email,password))
        data=cur.fetchone()
        cur.close()
        if data:
            return render_template("afterlogin.html",email=email,password=password)
        else:
            error="invalid email or password"
            return render_template("login.html",error=error)
        # return f"{email} and {password}"

@app.route("/aftersignup",methods=["post","GET"])
def aftersignup():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        con_password=request.form.get("con_password")
        if password==con_password:
            connect =sql.connect(host="localhost",port=3306,user="root",password="",database="weather_app")
            cur=connect.cursor()
            cur.execute("insert into signup(name,email,password,con_password) values(%s,%s,%s,%s) ",(name,email,password,con_password))
            connect.commit()
            cur.fetchall
            print(name)
            print(email)
            print(password)
            return render_template("afterlogin.html",email=email,password=password,name=name ,con_password=con_password)
        else :
            return "please enter same password"

app.run(debug=True,host="localhost",port=5500)

