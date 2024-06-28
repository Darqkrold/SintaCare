from flask import *  
import sqlite3 
import json 



app = Flask(__name__) 
app.secret_key = "secret123kjasjdkhkasd" 




conn = sqlite3.connect('database.db')
cursor = conn.cursor() 

sql = "CREATE TABLE IF NOT EXISTS USER (fullname varchar(255), email varchar(255), password varchar(255))"

cursor.execute(sql)

sql = "CREATE TABLE IF NOT EXISTS PatientRecords (request_id INTEGER PRIMARY KEY AUTOINCREMENT, patient_name varchar(255), date_of_first_admission varchar(255), date_of_last_admission varchar(255))"

cursor.execute(sql)

# request_id  - generation if login 

# REQUEST TABLE 

# request_Id 



@app.route("/")
def index(): 
    return render_template('index.html')

@app.route("/login", methods = ["GET", "POST"]) # URL 
def login():  # Controller 
    if request.method == "GET": 
        return render_template("login.html") 
    elif request.method == "POST": 
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor() 
        email = request.form.get("email") 
        password = request.form.get("password") 
        
        sql = "SELECT * FROM User WHERE email = ? AND password = ?" 
        
        result = cursor.execute(sql, (email, password))
        
        if (result.fetchall()): 
            # set session is_login 
            
            session['is_login'] = True
            return redirect("/records")
        else:
            return "Incorrect Username or Password"
        


@app.route("/register", methods = ["GET", "POST"]) 
def register(): 
    if request.method == "GET": 
   
        return render_template("register.html")
    
    elif request.method == "POST": 
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password == confirm_password: 
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor() 
            # fullname = 'OR '1' = '1'-- 
            
            
            # to prepare 
            
            
            sql = "INSERT INTO User (fullname, email, password) VALUES (?, ?, ?)"
            
            cursor.execute(sql, (fullname, email, password))
            conn.commit()
            
            return redirect("/login")
        else: 
            return "Password doesn't match"
        
        



@app.route("/logout")
def logout(): 
    session.pop('is_login', None)
    return redirect("/login")

@app.route("/records")
def records(): 
    if not session.get('is_login'): 
        return redirect("/login")
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    sql = "SELECT request_id, patient_name, date_of_first_admission FROM PatientRecords"
    
    result = cursor.execute(sql)
    result = result.fetchall()
    
    return render_template("records.html", records = result)


@app.route("/records/addPatient", methods = ["GET", "POST"])
def addPatient(): 
    if not session.get('is_login'): 
        return redirect("/login")
    if request.method == "GET": 
        return render_template("addPatient.html")
    elif request.method == "POST": 
        patient_name = request.form.get("fullname")
        date_of_first_admission = request.form.get("date")

        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor() 
        
        sql = "INSERT INTO PatientRecords (patient_name, date_of_first_admission) VALUES (?, ?)"
        
        cursor.execute(sql, (patient_name, date_of_first_admission))
        conn.commit()
        
        return redirect("/records")


@app.route("/records/deletePatient/<int:request_id>")
def deletePatient(request_id):
    if not session.get('is_login'): 
        return redirect("/login") 
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor() 
    
    sql = "DELETE FROM PatientRecords WHERE request_id = ?"
    
    cursor.execute(sql, (request_id,))
    conn.commit()
    
    return redirect("/records")

@app.route("/records/editPatient/<int:request_id>", methods = ["GET", "POST"])
def editPatient(request_id):
    if not session.get('is_login'): 
        return redirect("/login") 
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor() 
    
    if request.method == "GET": 
        sql = "SELECT * FROM PatientRecords WHERE request_id = ?"
        
        result = cursor.execute(sql, (request_id,))
        result = result.fetchone()
        
        return render_template("editPatient.html", patient = result)
    elif request.method == "POST": 
        patient_name = request.form.get("fullname")
        date_of_first_admission = request.form.get("date")
        
        sql = "UPDATE PatientRecords SET patient_name = ?, date_of_first_admission = ? WHERE request_id = ?"
        
        cursor.execute(sql, (patient_name, date_of_first_admission, request_id))
        conn.commit()
        
        return redirect("/records")
if __name__ == "__main__": 
    app.run(debug = True)