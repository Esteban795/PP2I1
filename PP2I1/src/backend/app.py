from flask import Flask,render_template, url_for,redirect,request
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
UPLOAD_FOLDER = './PP2I1/src/frontend/static/images/products/'

conn = sqlite3.connect("./PP2I1/src/backend/db/main.db", check_same_thread=False)
cursor = conn.cursor()

@login_manager.user_loader
def load_user(client_id : int):
    cursor.execute("SELECT client_id,first_name,last_name,email,pwd,created_at,recycled_volume,is_admin FROM clients WHERE client_id = ?", (client_id,))
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
        email : str = request.form['email']
        password : str = request.form['password']
        remember = request.form.get('remember-checkbox',-1) != -1
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
        redirect_endpoint = 'admin' if client.is_admin else 'home'
        login_user(client,remember=remember)
        return redirect(url_for(redirect_endpoint))
    else:
        return render_template('login.html')
    

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def getBinsInformation():
    bins_data = []
    DATA_FIELDS = ['first_name','last_name','lat','long','volume','used','last_emptied','created','waste_id','numberplate','waste_type']
    SQL = """
        SELECT first_name,last_name,lat,long,volume,used,last_emptied,created,waste_id,numberplate, name FROM bins
        JOIN clients ON bins.owner_id = clients.client_id
        LEFT JOIN trucks ON bins.last_emptied_by = trucks.truck_id
        JOIN waste_type ON bins.waste_id = waste_type.waste_type_id
    """
    #LEFT JOIN because some bins might have never been emptied yet!
    cursor.execute(SQL)
    bins = cursor.fetchall()
    for bin in bins:
        infos = {}
        for i in range(len(DATA_FIELDS)):
            infos[DATA_FIELDS[i]] = bin[i]
        bins_data.append(infos)
    return bins_data


def getProducts():
    products = []
    DATA_FIELDS = ['product_id','name','price','img_url','desc','volume','stock']
    SQL = """
        SELECT * FROM products
    """
    cursor.execute(SQL)
    temp = cursor.fetchall()
    for product in temp:
        infos = {}
        for i in range(len(DATA_FIELDS)):
            infos[DATA_FIELDS[i]] = product[i]
        products.append(infos)
    return products

@app.route('/admin/')
# @utilities.admin_required
def admin():
    error = request.args.get('error',None)
    bins_data = getBinsInformation()
    products = getProducts()
    return render_template('admin.html',bins_data=bins_data,products=products,error=error,purchases=[])

@app.route('/admin/add-product/',methods=('GET','POST'))
def add_product():
    if request.method == 'POST':
        name = request.form['product-name']
        price = request.form['price']
        volume = request.form['volume']
        desc = request.form['desc']
        stock = request.form['stock']
        f = request.files['img']
        if not utilities.checkValidInput(name,price,volume,desc,stock,f.filename):
            error = "Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ."
            return redirect(url_for('admin',error=error))
        file_uuid = utilities.generateImgUUID(f.filename)
        filepath = os.path.join(UPLOAD_FOLDER,file_uuid)
        f.save(filepath)
        cursor.execute("INSERT INTO products (name,price,volume,desc,stock,img_url) VALUES (?,?,?,?,?,?)",(name,price,volume,desc,stock,file_uuid))
        conn.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html') #no get request here

@app.route('/admin/modify-product/',methods=('GET','POST'))
def modify_product_not_selected():
    return redirect(url_for('admin',error="Veuillez sélectionner un produit à modifier."))

@app.route('/admin/modify-product/<int:product_id>',methods=('GET','POST'))
def modify_product(product_id : int):
    if request.method == 'POST':
        f = request.files['img']
        file_uuid = utilities.generateImgUUID(f.filename)
        if f.filename != '': #no picture was uploaded, use already existing one
            file_uuid = utilities.generateImgUUID(f.filename)
            filepath = os.path.join(UPLOAD_FOLDER,file_uuid)
            f.save(filepath)
            cursor.execute("SELECT img_url FROM products WHERE product_id = ?",(product_id,))
            old_pic = cursor.fetchone()[0]
            os.remove(os.path.join(UPLOAD_FOLDER,old_pic))
        name = request.form['product-name'] or None
        price = request.form['price'] or None
        volume = request.form['volume'] or None
        desc = request.form['desc'] or None
        stock = request.form['stock'] or None
        safe_filename = file_uuid if f.filename != '' else None #because empty word still has an uuid
        SQL = """
            UPDATE products 
            SET 
                name = coalesce(?,name),
                price = coalesce(?,price),
                volume = coalesce(?,volume),
                desc = coalesce(?,desc),
                stock = coalesce(?,stock),
                img_url = coalesce(?,img_url)
            WHERE product_id = ?
        """
        cursor.execute(SQL,(name,price,volume,desc,stock,safe_filename,product_id))
        conn.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html') #no get request here

@app.route('/admin/delete/<int:product_id>',methods=('GET','POST'))
def delete_product(product_id : int):
    if request.method == 'POST':
        cursor.execute("SELECT img_url FROM products WHERE product_id = ?",(product_id,))
        filename = cursor.fetchone()[0]
        filepath = os.path.join(UPLOAD_FOLDER,filename)
        os.remove(filepath)
        cursor.execute("DELETE FROM products WHERE product_id = ?",(product_id,))
        conn.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)