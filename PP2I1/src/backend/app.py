from flask import Flask, render_template, url_for,redirect,request,session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3
import hashlib
import os
import datetime

from knapsack import knapsack
from tsp_simulated_annealing import TSPSolver as saTSPSolver
from Client import Client
import utilities
import datetime as dt

app = Flask(__name__,template_folder="../frontend/templates",static_folder="../frontend/static")
app.config["SECRET_KEY"] = os.urandom(24)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
UPLOAD_FOLDER = './PP2I1/src/frontend/static/images/products/'

conn = sqlite3.connect("./PP2I1/src/backend/db/main.db", check_same_thread=False)
cursor = conn.cursor()

BASE_COORDS = (49.133333,6.166667)
CREATION_DATE = dt.datetime(2015,11,1)

@login_manager.user_loader
def load_user(client_id : int):
    cursor.execute("SELECT client_id,first_name,last_name,email,pwd,created_at,recycled_volume,status FROM clients WHERE client_id = ?", (client_id,))
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
        login_user(client,remember=remember)
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
            lats,longs = utilities.checkValidAdresses(adresses)
            if not lats:
                return redirect(url_for("cart_validation",error="Une des adresses est invalide."))
            cursor.executemany("INSERT INTO bins(owner_id,product_id,lat,long,waste_id) VALUES (?,?,?,?,?)",[(current_user.client_id,product_id,lat,long,1) for product_id,lat,long in zip(products_ids,lats,longs)])
            conn.commit()
        else:
            lat,long = utilities.checkValidAdresses([adresses[0]])
            if not lat:
                return redirect(url_for("cart_validation",error="L'adresse est invalide."))
            lat,long = lat[0],long[0]
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

def getTrucks():
    trucks = []
    DATA_FIELDS = ['truck_id','numberplate','capacity']
    SQL = """
        SELECT * FROM trucks
    """
    cursor.execute(SQL)
    temp = cursor.fetchall()
    for truck in temp:
        infos = {}
        for i in range(len(DATA_FIELDS)):
            infos[DATA_FIELDS[i]] = truck[i]
        trucks.append(infos)
    return trucks

def getBinsInformation():
    bins_data = []
    DATA_FIELDS = ['first_name','last_name','lat','long','volume','used','last_emptied','bought_at','numberplate','waste_type_name','product_name']
    SQL = """
        SELECT first_name,last_name,lat,long,volume,used,last_emptied,bought_at,numberplate, waste_type_name,product_name FROM bins
        JOIN clients ON bins.owner_id = clients.client_id
        JOIN products ON bins.product_id = products.product_id
        LEFT JOIN waste_type ON bins.waste_id = waste_type.waste_type_id
        LEFT JOIN trucks ON bins.last_emptied_by = trucks.numberplate
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

def getWasteTypes():
    waste_types = []
    DATA_FIELDS = ['waste_id','waste_type_name']
    SQL = """
        SELECT * FROM waste_type
    """
    cursor.execute(SQL)
    temp = cursor.fetchall()
    for product in temp:
        infos = {}
        for i in range(len(DATA_FIELDS)):
            infos[DATA_FIELDS[i]] = product[i]
        waste_types.append(infos)
    return waste_types

def getAllPurchases():
    purchases = []
    DATA_FIELDS = ['bin_id','first_name','last_name','email','bought_at','price']
    SQL = """
        SELECT bin_id,first_name,last_name,email,bought_at,price FROM bins
        JOIN clients ON bins.owner_id = clients.client_id
        JOIN products ON bins.product_id = products.product_id
    """
    cursor.execute(SQL)
    temp = cursor.fetchall()
    for purchase in temp:
        infos = {}
        for i in range(len(DATA_FIELDS)):
            infos[DATA_FIELDS[i]] = purchase[i]
        purchases.append(infos)
    return purchases

@app.route('/admin/')
#@utilities.admin_required
def admin():
    route = session.get('route',None)
    error = request.args.get('error',None)
    derror = request.args.get('derror',None)
    bins_data = getBinsInformation()
    products = getProductsList()
    waste_types = getWasteTypes()
    purchases = getAllPurchases()
    trucks = getTrucks()
    return render_template('admin.html',trucks=trucks,route=route,bins_data=bins_data,products=products,error=error,waste_types=waste_types,purchases=purchases,derror=derror)

@app.route('/admin/add-product/',methods=('GET','POST'))
#@utilities.admin_required
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
        cursor.execute("INSERT INTO products (product_name,price,volume,desc,stock,img_url) VALUES (?,?,?,?,?,?)",(name,price,volume,desc,stock,file_uuid))
        conn.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html') #no get request here

@app.route('/admin/modify-product/',methods=('GET','POST'))
#@utilities.admin_required
def modify_product_not_selected():
    return redirect(url_for('admin',error="Veuillez sélectionner un produit à modifier."))

@app.route('/admin/modify-product/<int:product_id>',methods=('GET','POST'))
#@utilities.admin_required
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
                product_name = coalesce(?,product_name),
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
#@utilities.admin_required
def delete_product(product_id : int):
    if request.method == 'POST':
        cursor.execute("SELECT img_url FROM products WHERE product_id = ?",(product_id,))
        filename = cursor.fetchone()[0]
        filepath = os.path.join(UPLOAD_FOLDER,filename)
        os.remove(filepath)
        cursor.execute("DELETE FROM products WHERE product_id = ?",(product_id,))
        conn.commit()
    return redirect(url_for('admin'))

@app.route('/admin/add-transaction/',methods=('GET','POST'))
#@utilities.admin_required
def add_transaction_not_selected():
    return redirect(url_for('admin',derror="Veuillez sélectionner un produit."))

@app.route('/admin/add-transaction/<int:product_id>',methods=('GET','POST'))
#@utilities.admin_required
def add_transaction(product_id : int):
    if request.method == 'POST':
        date = request.form['date-transac']
        email = request.form['email']
        lat = request.form['latitude']
        long = request.form['longitude']
        if not utilities.checkValidInput(date,email,lat,long):
            return redirect(url_for('admin',derror="Veuillez remplir tous les champs ou ne pas utiliser que des espaces dans un champ."))
        waste_type_id = request.form['waste-type']
        cursor.execute("SELECT client_id FROM clients WHERE email = ?",(email,))
        client_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO bins (owner_id,product_id,lat,long,waste_id,bought_at) VALUES (?,?,?,?,?,?)",(client_id,product_id,lat,long,waste_type_id,date))
        conn.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('admin')) #get request redirected directly

@app.route("/admin/purchases/delete-transaction/<int:bin_id>",methods=('GET','POST'))
#@utilities.admin_required
def delete_purchase(bin_id : int):
    if request.method == 'POST':
        cursor.execute("DELETE FROM pickup WHERE bin_id = ?",(bin_id,))
        cursor.execute("DELETE FROM bins WHERE bin_id = ?",(bin_id,))
        conn.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))

@app.route('/admin/purchases/modify-purchases/<int:bin_id>',methods=('GET','POST'))
#@utilities.admin_required
def modify_purchase(bin_id : int):
    pass

@app.route("/admin/start-pickup/",methods=('GET','POST'))
#@utilities.admin_required
def start_pickup():
    if request.method == 'POST':
        truck_numberplate = request.form['truck']
        SQL = """
            SELECT capacity FROM trucks WHERE numberplate = ?
        """
        cursor.execute(SQL,(truck_numberplate,))
        maxcapacity = cursor.fetchone()[0]
        SQL = """
            SELECT lat,long,volume,used,bin_id FROM bins
            JOIN products ON products.product_id = bins.product_id
            GROUP BY lat,long
        """
        cursor.execute(SQL)
        db_results = cursor.fetchall()
        if not db_results: #db is empty
            return redirect(url_for('admin'))
        bins_ids = [x[4] for x in db_results]
        bins_coords = [(x[0],x[1]) for x in db_results]
        bins_volume = [x[2] for x in db_results]
        bins_used_volume = [x[3] for x in db_results]
        weight_used,chosen_bins = knapsack(maxcapacity,bins_used_volume,[100 * bins_used_volume[i] / bins_volume[i] for i in range(len(bins_volume)) ])
        chosen_bins = [True for i in range(len(db_results))]
        chosen_bins = [bins_coords[i] for i in range(len(chosen_bins)) if chosen_bins[i]]
        chosen_bins_ids = [bins_ids[i] for i in range(len(chosen_bins)) if chosen_bins[i]]
        chosen_bins_used = [bins_used_volume[i] for i in range(len(chosen_bins)) if chosen_bins[i]]
        chosen_bins.append(BASE_COORDS)
        tsp_solver = saTSPSolver(chosen_bins,utilities.getHaversineDistance)
        tsp_res,best_route_length = tsp_solver.simulatedAnnealing()
        base_coords_index = tsp_res.index(len(chosen_bins) - 1)
        tsp_res = [chosen_bins[i] for i in tsp_res]
        session['route'] = utilities.circularTranslationArray(tsp_res,base_coords_index)
        for i in range(len(chosen_bins_ids)):
            cursor.execute("UPDATE bins SET last_emptied_by = ?, last_emptied = ? WHERE bin_id = ?",(truck_numberplate,datetime.datetime.now().replace(microsecond=0),chosen_bins_ids[i]))
            cursor.execute("INSERT INTO pickup(truck_id,bin_id,picked_up) VALUES (?,?,?)",(truck_numberplate,chosen_bins_ids[i],chosen_bins_used[i]))
        conn.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))


@app.route('/admin/ban-user', methods=('GET','POST')) 
#@utilities.admin_required
def ban_user(client_id: int):
    if request.method == 'POST':
        cursor.execute('UPDATE clients SET status = ? WHERE client_id = ? ',(-1, client_id))
        conn.commit()
        redirect(url_for('admin'))
    return render_template('admin.html')

@app.route('/admin/unban-user', methods=('GET','POST')) 
#@utilities.admin_required
def unban_user(client_id: int):
    if request.method == 'POST':
        cursor.execute('UPDATE clients SET status = ? WHERE client_id = ? ',(0, client_id))
        conn.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html')

@app.route('/admin/user-to-admin', methods=('GET','POST')) 
#@utilities.admin_required
def user_to_admin(client_id: int):
    if request.method == 'POST':
        cursor.execute('UPDATE clients SET status = ? WHERE client_id = ?', (1, client_id))
        conn.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html')

def getPurchases(client_id):
    DATA_FIELDS = ['bin_id','first_name','last_name','email','bought_at','price']
    SQL = """
        SELECT bin_id,first_name,last_name,email,bought_at,price FROM bins 
        JOIN clients ON bins.owner_id = clients.client_id 
        JOIN products ON bins.product_id = products.product_id 
        WHERE owner_id = ?
    """
    cursor.execute(SQL,(client_id,))
    temp = cursor.fetchall()
    return [dict(zip(DATA_FIELDS,purchase)) for purchase in temp]

def getBinsCount(client_id):
    SQL = "SELECT COUNT(*) FROM bins WHERE owner_id = ?"
    cursor.execute(SQL,(client_id,))
    return cursor.fetchone()[0]

def getVolumeInfos(client_id):
    FIELDS = ["picked_up_volume","recycled_volume"]
    SQL = f"SELECT {','.join(FIELDS)} FROM clients WHERE client_id = ?"
    cursor.execute(SQL,(client_id,))
    res = cursor.fetchone()
    return dict(zip(FIELDS,res))

def getBinsStats(client_id : int,time_since_creation) -> dict:
    FIELDS = ["used","bought_at","volume","img_url",'lat','long']
    bins_infos = []
    SQL = """
        SELECT used,bought_at,volume,img_url,lat,long FROM bins
        JOIN products ON bins.product_id = products.product_id
        WHERE owner_id = ?
    """
    cursor.execute(SQL,(client_id,))
    bins = cursor.fetchall()
    for bin in bins:
        infos = {}
        for i in range(len(FIELDS)):
            infos[FIELDS[i]] = bin[i]
        dtime = dt.datetime.strptime(infos["bought_at"],"%Y-%m-%d %H:%M:%S")
        nb_days_since_bought = (dt.datetime.now() - dtime).days
        infos["existence_time_percentage"] = nb_days_since_bought / time_since_creation
        infos["bought_at"] = dt.datetime.now().year - dtime.year
        bins_infos.append(infos)
    return bins_infos


@app.route('/profile/')
@login_required
def profile():
    current_user_id = current_user.client_id
    bins_count = getBinsCount(current_user_id)
    volume_infos = getVolumeInfos(current_user_id)
    recycled_percentage = 100 * volume_infos["recycled_volume"] / volume_infos["picked_up_volume"] if volume_infos["picked_up_volume"] != 0 else 0
    time_since_creation = (dt.datetime.now() - CREATION_DATE).days
    bins_infos = getBinsStats(current_user_id,time_since_creation)
    purchases = getPurchases(current_user_id)
    return render_template('profile.html',user=current_user,bins_count=bins_count,volume_infos=volume_infos,joined_at=current_user.created_at.year,recycled_percentage=recycled_percentage,bins_infos=bins_infos,time_since_creation=time_since_creation,purchases=purchases)

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
        
        cursor.execute("SELECT bin_id FROM bins WHERE owner_id = ?",(current_user_id,))
        bins_ids = cursor.fetchall()
        cursor.executemany("DELETE FROM pickup WHERE bin_id = ?",bins_ids)
        cursor.execute("DELETE FROM bins WHERE owner_id = ?",(current_user_id,))
        cursor.execute("DELETE FROM clients WHERE client_id = ?",(current_user_id,))
        conn.commit()
        return redirect(url_for('login'))
    return redirect(url_for('profile'))

@app.route('/profile/reset-password/',methods=('GET','POST'))
@login_required
def reset_password():
    current_user_id = current_user.client_id
    if request.method == 'POST':
        confirm_password = request.form['password']
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