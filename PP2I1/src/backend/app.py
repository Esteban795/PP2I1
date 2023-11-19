from flask import Flask, render_template, url_for,redirect,request,flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3

from Client import Client


app = Flask(__name__,template_folder="../frontend/templates",static_folder="../frontend/static")
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
login_manager = LoginManager(app)
login_manager.login_view = 'login'

conn = sqlite3.connect("./PP2I1/src/backend/db/main.db", check_same_thread=False)
cursor = conn.cursor()

@login_manager.user_loader
def load_user(client_id : int):
    cursor.execute("SELECT client_id,first_name,last_name,email,pwd FROM clients WHERE client_id = ?", (client_id,))
    db_data = cursor.fetchone()
    if db_data is not None:
        client = Client(*db_data)
        return client
    return None

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup/', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password-repeat']

        #check if email already exists
        cursor.execute("SELECT email FROM clients WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result is None:
            if password == password_confirm:
                cursor.execute("INSERT INTO clients (first_name,last_name,email,pwd) VALUES (?,?,?,?)",
                               (first_name,last_name,email,password))
                conn.commit()
                return redirect(url_for('login'))
            else:
                flash('Passwords do not match.','error')
                return redirect(url_for('signup'))
        else:
            flash('Email already exists. Might want to login instead ?','error')
            return redirect(url_for('signup'))
    elif request.method == 'GET':
        return render_template('sign_up.html')

@app.route('/login/', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        pass
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)