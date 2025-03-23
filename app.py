from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configurations (Set to match your XAMPP MySQL setup)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Default user in XAMPP
app.config['MYSQL_PASSWORD'] = ''  # Default password is empty
app.config['MYSQL_DB'] = 'flask_auth'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    if 'username' in session:
        return f"<h1>Hi, {session['username']}! <a href='/logout'>Logout</a></h1>"
    return "<h1>Welcome! <a href='/login'>Login</a> | <a href='/signup'>Signup</a></h1>"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid Credentials"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


print(f"Python Version: {os.sys.version}")
      

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)