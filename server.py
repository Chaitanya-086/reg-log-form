from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__,template_folder='Templates')
def create_database(): 

    connection = sqlite3.connect("users_v3.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
create_database()

@app.route("/",methods=["GET"])
def home():
    return render_template("navbar.html",page="home")

@app.route("/home")
def home_page():
    return render_template("home.html",page="home_page")

@app.route("/employee")
def employees():
    return render_template("employee.html", page="employee")

@app.route("/addemployee")
def add_employee_page():
    return render_template("addemployee.html", page="add")
@app.route("/addemployee",methods=["POST"])
def add_employee():
    name=request.form["name"]
    email=request.form["email"]
    phone_number=request.form["phone_number"]
    department=request.form["department"]
    salary=request.form["salary"]
    Joining_Date=request.form["Joining_Date"]
    address=request.form["address"]
    connection=sqlite3.connect("users_v3.db")
    cursor=connection.cursor()

    cursor.execute("""
       INSERT INTO employee
       (name,email,phone_number,department,salary,Joining_Date,address)
       VALUES(?,?,?,?,?,?,?)
       """,(
        name,email,phone_number,department,salary,Joining_Date,address
       ))
    connection.commit()
    connection.close()
    return """
    <h2> Employee added successfully!</h2>
    <br>
    <a href="/addemployee">Add another employee</a>
    <br><br>
    <a href="/">Go to home</a>
    """
@app.route("/search")
def search():
    return render_template("search.html", page="search")

@app.route("/register", methods=["GET"])
def registers():
    return render_template("register.html", page="registers")


@app.route("/login",methods=["GET"])
def logins():
    return render_template("login.html",page="logins")

 
# -----------------------------------
# Add Employee Path
# -----------------------------------

@app.route("/addemployee", methods=["GET"])
def register_page():
    return render_template("addemployee.html")
@app.route("/register", methods=["POST"])
def register():

    fullname = request.form.get("fullname")
    username = request.form.get("username")
    password = request.form.get("password")

    connection = sqlite3.connect("users_v3.db")

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (fullname, username, password)
            VALUES (?, ?, ?)
        """, (fullname, username, password))

        connection.commit()
        connection.close()
        return "<h2>Registration Successful!</h2><a href='/login'>Go to Login</a>"

    except sqlite3.IntegrityError:

        connection.close()

        return """
        <h2>Username already exists!</h2>
        <a href="/register">Try Again</a>
        """


@app.route("/login", methods=["GET"])
def login_page():

    return render_template("login.html")

 
# -----------------------------------
# Login Path
# -----------------------------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    connection = sqlite3.connect("users_v3.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    connection.close()

    if user:

        return """
        <h2>Login successful!</h2>
        <p>Welcome, """ + username + """!</p>
        <a href="/">Go to Home</a>
        """

    else:

        return """
        <h2>Login failed!</h2>
        <p>Username or password is incorrect.</p>
        <a href="/login">Try Again</a>
        """


if __name__ == "__main__":

    create_database()


    app.run(debug=True)