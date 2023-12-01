from flask import Flask, session, flash, render_template, url_for,redirected,request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3


conn = sqlite3.connect("./PP2I1/src/backend/db/main.db")
cursor = conn.cursor()

app = Flask(__name__,template_folder="../frontend/templates",static_folder="../frontend/static")

@app.route('/shop', methods =('GET', 'POST'))
def add_cart_to_db():
    ids = session['cart'] #items

    if request.method == 'POST':
        current_user_id = current_user.id

        data = []

        for id in ids:
            data.append((id, current_user_id))

        cursor.executemany("INSERT INT0 bins (bin_id, owner_id) VALUES (?,?) ", data)
        conn.commit()
    return redirected(url_for('home'))




