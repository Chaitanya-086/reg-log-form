import sqlite3
from flask import Flask,render_template,request,redirect
app=Flask(__name__)
def create_database():
    #connect to datebase
    connection=sqlite3.connect("users.db")
    #store database in some objects
    cursor=connection.cursor()
    #write query using that object
    cursor.execute(
      """ create table if not exists user(
       id integer primary key
       autoincrement,
       fullname text not null,
       username text unique notnull,
       password text notnull,
       ) 
       """)
    #commit query
    connection.commit()
    #close connection
    connection.close()
@app.route("/")
def home():
    return render_template("register2.html")
if __name__=="__main__":
    app.run(debug=True)
@app.route("/register",method=["POST"])
def register():
    return render_template("register2.html")
fullname=request.form["fullname"]
username=request.form["username"]
password=request.form["password"]
connection=sqlite3.connect("users.db")
cursor=connection.cursor()
cursor.execute("""
        INSERT INTO user(fullname,username,password
        VALUES(???)
        """,)(fullname,username,)