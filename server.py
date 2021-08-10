from datetime import timedelta
from flask import Flask, json, render_template, redirect, url_for, request
from flask.globals import session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'mcaproject'


# connected to mysql database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'miniproject'

mysql = MySQL(app)

@app.route('/')
def index():
    if 'isLoggedIn' in session:  
        cur = mysql.connection.cursor()
        student = cur.execute("SELECT * FROM student")
        if student > 0:
            stuDetails = cur.fetchall()
            return render_template("index.html", stuDetails = stuDetails)
        else:
            return render_template('index.html')
    else:
        return redirect("/login")
    

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        roll_no = request.form['roll_no']
        year = request.form['year']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student(name,email,phone,course,roll_no,year) VALUES(%s,%s,%s,%s,%s,%s)",
                    (name, email, phone, course, roll_no, year))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
        
    return render_template('add.html', title="Add Student")

@app.route('/update/<id>', methods=['GET','POST'])
def update(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        roll_no = request.form['roll_no']
        year = request.form['year']
        id = request.form['id']
        
        cur1 = mysql.connection.cursor()
        cur1.execute("UPDATE student SET name=%(name)s, email=%(email)s, phone=%(phone)s, course=%(course)s, roll_no=%(roll_no)s, year=%(year)s WHERE id=%(id)s ",
                     {'name':name, 'email':email, 'phone':phone, 'course':course, 'roll_no':roll_no, 'year':year, 'id':id})
        mysql.connection.commit()
        cur1.close()
        
        return redirect('/')
        
    cur = mysql.connection.cursor()
    data = cur.execute("SELECT * FROM student WHERE id=%(id)s", {'id':id})
    if data > 0:
        student = cur.fetchone()
    return render_template('update.html', title="Update Student", student = student)

@app.route('/delete/<id>', methods=["POST","GET"])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE id=%(id)s",{'id':id})
    mysql.connection.commit()
    cur.close()
    
    return redirect('/');

@app.route('/search', methods=["GET","POST"])
def search():
    if request.method == "POST":
        search = request.form['search']
        
        cur = mysql.connection.cursor()
        data = cur.execute("SELECT * FROM student WHERE roll_no=%(search)s",{'search':search})
        if data > 0:
            student = cur.fetchone()
            return render_template('search.html',student = student)
        else:
            return  redirect('/')
        
@app.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']
        if name != '' and email !='' and password !='' and cpassword !='':
            if password == cpassword:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO signup(name,email,password) VALUES(%s,%s,%s)",(name, email, password))
                mysql.connection.commit()
                cur.close()
                return render_template("signup.html", msg="You are successfully signed up, go to login")
            else:
                return render_template("signup.html", msg="password did not match")
        else:
            return render_template("signup.html", msg="some fields are empty")
        
    return render_template("signup.html")


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email !='' and password !='':
            cur = mysql.connection.cursor()
            data = cur.execute("SELECT * FROM signup WHERE email=%(email)s AND password=%(password)s",{'email':email, 'password':password})
            if data > 0:
                session['isLoggedIn'] = 'true'
                return redirect("/")
            else:
                return render_template("login.html", msg="no records found matching your query")
            
        else:
            return render_template("login.html", msg="some fields are empty")
        
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('isLoggedIn', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    
    app.run(debug=True)