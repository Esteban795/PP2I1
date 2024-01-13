from flask import Flask, render_template, url_for,redirect,request,session
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

# Static files loader. Makes working with subroutes **much easier**
@app.route("/static/css/<fichier>")
def send_css(fichier : str):
    return app.send_static_file(f"./css/{fichier}")

@app.route("/static/js/<fichier>")
def send_js(fichier : str):
    return app.send_static_file(f"./js/{fichier}")

@app.route("/static/images/<fichier>")
def send_images(fichier : str):
    return app.send_static_file(f"./images/{fichier}")

@app.route('/')
def home():
    return render_template('base.html')

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
        return redirect(request.args.get("next") or url_for('home')) #redirect to the previous page in case of successful login
    else:
        return render_template('login.html')
    

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(request.args.get("next") or url_for('home')) 

def getProductsList():
    FIELDS = ["product_id","product_name","price","img_url","desc","volume","stock"]
    cursor.execute("SELECT {} FROM products".format(",".join(FIELDS)))
    products = cursor.fetchall()
    products = [dict(zip(FIELDS,product)) for product in products]
    return products


@app.route('/shop/', methods=['GET','POST'])
def shop():
    if request.method == "POST":
        cart = request.form["cart"]
        products_ids = [int(i) for i in cart.split("-")]
        session["products_ids"] = utilities.runLengthEncoding(sorted(products_ids)) # dict {product_id : quantity}
        return redirect(url_for("cart_validation"))
    products = getProductsList()
    return render_template('shop.html',products=products)

@app.route("/shop/cart-validation/",methods=['GET','POST'])
@login_required
def cart_validation():
    session.modified = False
    if request.method == "POST":
        check_same_adress = request.form.get("use-same-adress",None)
        adresses = request.form.getlist("adress")
        products_ids = session.get("products_ids",None)
        if products_ids is None:
            return redirect(url_for("shop"))
        products_ids = utilities.runLengthDecoding(products_ids)
        if check_same_adress is None: #checkbox is unchecked
            if any([adress == "" for adress in adresses]):
                return redirect(url_for("cart_validation",error="Veuillez remplir tous les formulaires d'adresses."))
            lats,longs = [],[]
            for adress in adresses:
                lat,long = utilities.getLatLongFromStreetAdress(adress)
                lats.append(lat)
                longs.append(long)
            cursor.executemany("INSERT INTO bins(owner_id,product_id,lat,long,waste_id) VALUES (?,?,?,?,?)",[(current_user.client_id,product_id,lat,long,1) for product_id,lat,long in zip(products_ids,lats,longs)])
            conn.commit()
        else:
            if adresses[0] == "":
                return redirect(url_for("cart_validation",error="Veuillez remplir l'adresse."))
            lat,long = utilities.getLatLongFromStreetAdress(adresses[0])
            cursor.executemany("INSERT INTO bins(owner_id,product_id,lat,long,waste_id) VALUES (?,?,?,?,?)",[(current_user.client_id,product_id,lat,long,1) for product_id in products_ids])
            conn.commit()
        return redirect(url_for("cart_success"))
    products = getProductsList()
    final_products = []
    products_ids = session.get("products_ids",[])
    for i in products_ids:
        for j in products:
            if int(i) == j["product_id"]:
                for k in range(session["products_ids"][i]):
                    final_products.append(j)
    error = request.args.get('error',None)
    return render_template("cart_validation.html",cart=final_products,error=error)

@app.route("/shop/purchase-cart/success/",methods=['GET','POST'])
def cart_success():
    products = getProductsList()
    final_products = []
    for i in session["products_ids"]:
        for j in products:
            if int(i) == j["product_id"]:
                for k in range(session["products_ids"][i]):
                    final_products.append(j)
    return render_template("cart_success.html",products=final_products)

def getUserProducts(client_id):
    products = []
    DATA_FIELDS = ['client_id','bin_id','price', 'date']
    SQL = f"SELECT * FROM purchases WHERE client_id = {client_id}"
    cursor.execute(SQL)
    temp = cursor.fetchall()
    for product in temp:
        infos = {}
        for i in range(len(DATA_FIELDS)):
            infos[DATA_FIELDS[i]] = product[i]
        products.append(infos)
    return products

def getPurchases(client_id):
    purchases = []
    DATA_FIELDS = ['bin_id','first_name','last_name','email','bought_at','price']
    SQL = "SELECT bin_id,first_name,last_name,email,bought_at,price FROM bins JOIN clients ON bins.owner_id = clients.client_id JOIN products ON bins.product_id = products.product_id WHERE owner_id = ?"
    cursor.execute(SQL,(client_id,))
    temp = cursor.fetchall()
    for purchase in temp:
        infos = {}
        for i in range(len(DATA_FIELDS)):
            infos[DATA_FIELDS[i]] = purchase[i]
        purchases.append(infos)
    return purchases

@app.route('/profile/')
#@login_required
def profile():
    current_user_id = current_user.client_id
    return render_template('profile.html',user=current_user, recycled_volume=10, total_volume=20, recycled_percentage=50)

@app.route('/profile/delete-user/',methods=('GET','POST'))
@login_required
def delete_user():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        confirm_password = request.form['password']
        if not utilities.checkValidInput(confirm_password):
            return render_template('profile.html',user = current_user,error_deleteuser="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.",recycled_volume=10, total_volume=20, recycled_percentage=50)
        hash_object = hashlib.sha256(confirm_password.encode('utf-8'))
        confirm_password = hash_object.hexdigest()
        if current_user.password != confirm_password:
            return render_template('profile.html',error_deleteuser="Le mot de passe est incorrect.",user=current_user, recycled_volume=10, total_volume=20, recycled_percentage=50)
        cursor.execute('UPDATE clients SET first_name = ?, last_name = ?, email = ?, created_at = ?, pwd = ?, recycled_volume = ?, status = ? WHERE client_id = ?', (None, None, None, None, None,None, None, current_user_id))
        conn.commit()
        redirect(url_for('login'))
    return render_template('homepage.html',user=current_user)

@app.route('/profile/reset-password/',methods=('GET','POST'))
@login_required
def reset_password():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        confirm_password = request.form['confirm-password']
        new_password = request.form['new-password']
        if not utilities.checkValidInput(new_password, confirm_password):
            return render_template('profile.html',user = current_user,error_passwordreset="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.",recycled_volume=10, total_volume=20, recycled_percentage=50)
        hash_object = hashlib.sha256(confirm_password.encode('utf-8'))
        confirm_password = hash_object.hexdigest()
        if current_user.password != confirm_password:
            return render_template('profile.html',error_passwordreset='Le mot de passe est incorrect',user=current_user, recycled_volume=10, total_volume=20, recycled_percentage=50)
        hash_object = hashlib.sha256(new_password.encode('utf-8'))
        hashed_pass = hash_object.hexdigest()
        cursor.execute('UPDATE clients SET pwd = ? WHERE client_id = ?', (hashed_pass,current_user_id))
        conn.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html',user = current_user,recycled_volume=10, total_volume=20, recycled_percentage=50)

@app.route('/profile/reset-first-name/', methods=('GET', 'POST'))
@login_required
def reset_first_name():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        new_first_name = request.form['new-first-name']
        if not utilities.checkValidInput(new_first_name):
            return render_template('profile.html',user=current_user,error_name="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.",recycled_volume=10, total_volume=20, recycled_percentage=50)
        cursor.execute('UPDATE clients SET first_name = ? WHERE client_id = ?', (new_first_name,current_user_id))
        conn.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html', user = current_user,recycled_volume=10, total_volume=20, recycled_percentage=50)

@app.route('/profile/reset-last-name/', methods=('GET', 'POST'))
@login_required
def reset_last_name():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        new_last_name = request.form['new-last-name']
        if not utilities.checkValidInput(new_last_name):
            return render_template('profile.html',user=current_user,error_name="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.",recycled_volume=10, total_volume=20, recycled_percentage=50)
        cursor.execute('UPDATE clients SET last_name = ? WHERE client_id = ?', (new_last_name,current_user_id))
        conn.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html', user = current_user,recycled_volume=10, total_volume=20, recycled_percentage=50)


@app.route('/profile/reset-email/', methods=('GET','POST'))
@login_required
def reset_email():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        new_email = request.form['new-email']
        if not utilities.checkValidInput(new_email):
            return render_template('profile.html',user=current_user,error="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ.",recycled_volume=10, total_volume=20, recycled_percentage=50)
        cursor.execute('UPDATE clients SET email = ? WHERE client_id = ?',(new_email, current_user_id))
        conn.commit()
        return redirect(url_for('profile'))
    return render_template('profile.html', user = current_user,recycled_volume=10, total_volume=20, recycled_percentage=50)


if __name__ == '__main__':
    app.run(debug=True, port=8080)