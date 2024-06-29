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
