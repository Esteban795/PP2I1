from flask import Flask, render_template, url_for,redirect,request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3
import hashlib
import os


from Client import Client
import utilities

app = Flask(__name__,template_folder="../frontend/templates",static_folder="../frontend/static")
app.config["SECRET_KEY"] = os.urandom(24)
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
def home():
    return render_template('home.html')

@app.route('/signup/', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password-repeat']
        if not utilities.checkValidInput(first_name,last_name,email,password,password_confirm):
            return render_template('sign_up.html',error="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.")
        else:
            cursor.execute("SELECT email FROM clients WHERE email = ?", (email,))
            result = cursor.fetchone()
            if result is not None: #someone already has this email registered
                return render_template('sign_up.html',error='Cette adresse email est déjà utilisée.')
            elif password != password_confirm: #passwords do not match
                return render_template('sign_up.html',error="Les mots de passe ne correspondent pas.")
            
            hash_object = hashlib.sha256(password.encode('utf-8'))
            hashed_pass = hash_object.hexdigest()
            cursor.execute("INSERT INTO clients (first_name,last_name,email,pwd) VALUES (?,?,?,?)",(first_name,last_name,email,hashed_pass))
            conn.commit()
            return redirect(url_for('login'))
    return render_template('sign_up.html')


@app.route('/login/', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not utilities.checkValidInput(email,password):
            return render_template('login.html',error="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.")
        
        cursor.execute("SELECT * FROM clients WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user is None:
            return render_template('login.html',error="Cette adresse email n'est liée à aucun compte.")
        
        client = Client(*user)
        hash_object = hashlib.sha256(password.encode('utf-8'))
        password = hash_object.hexdigest()
        if client.password != password:
            return render_template('login.html',error="Le mot de passe est incorrect.")
        login_user(client)
        return redirect(url_for('home'))
    else:
        return render_template('login.html')
    

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile/')
@login_required
def profile():
    return render_template('profile.html',user=current_user, recycled_volume=10, total_volume=20, recycled_percentage=50)

@app.route('/profile/delete-user/',methods=('GET','POST'))
@login_required
def delete_user():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        cursor.execute('UPDATE clients SET first_name = ?, last_name = ?, creat_at = ?, pwd = ?, recycled_volume = ?, status = ? WHERE client_id = ?', (None, None, None, None,None, None, current_user_id))
        conn.commit()
        redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/profile/reset-first-name/', methods=('GET', 'POST'))
@login_required
def reset_first_name():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        new_first_name = request.form['new-first-name']
        if not utilities.checkValidInput(new_first_name):
            return render_template('profile.html',error="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.")
        cursor.execute('UPDATE clients SET first_name = ? WHERE client_id = ?', (new_first_name,current_user_id))
        conn.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/profile/reset-last-name/', methods=('GET', 'POST'))
@login_required
def reset_last_name():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        new_last_name = request.form['new-last-name']
        if not utilities.checkValidInput(new_last_name):
            return render_template('profile.html',error="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.")
        cursor.execute('UPDATE clients SET last_name = ? WHERE client_id = ?', (new_last_name,current_user_id))
        conn.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html', recycled_volume=10, total_volume=20, recycled_percentage=50)


@app.route('/profile/reset-email/', methods=('GET','POST'))
@login_required
def reset_email():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        new_email = request.form['new-email']
        if not utilities.checkValidInput(new_email):
            return render_template('profile.html',error="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.")
        cursor.execute('UPDATE clients SET email = ? WHERE client_id = ?',(new_email, current_user_id))
        conn.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html', recycled_volume=10, total_volume=20, recycled_percentage=50)


if __name__ == '__main__':
    app.run(debug=True, port = 8080)
