from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector as db

mydb = db.connect(host='localhost', user='root', password="Mahesh@123", db='hackathon')
cur = mydb.cursor()

app = Flask(__name__)
app.secret_key = 'super_secret_key'  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/user_register', methods=["GET", "POST"])
def userRegister():
    user_name = request.form['u_name']
    user_email = request.form['u_email']
    user_phone = request.form['phone']
    user_address = request.form['u_address']
    user_credit = request.form['credit']
    user_pwd = request.form['u_pwd']

    try:
        cur.execute("INSERT INTO users(user_name, user_email, user_phone, user_address, user_credit, user_pwd) VALUES (%s, %s, %s, %s, %s, %s)",
                    (user_name, user_email, user_phone, user_address, user_credit, user_pwd))
        mydb.commit()
        return render_template('register_success.html', message="Registration Successful! Thank you for registering.")
    except:
        return render_template('register_success.html', message="Failed while registering. Please try again.")

@app.route('/user_login', methods=["POST", "GET"])
def userLogin():
    u_email = request.form['user_email']
    u_pwd = request.form['pwd']
    cur.execute("SELECT user_name FROM users WHERE user_email=%s AND user_pwd=%s", (u_email, u_pwd))
    user_data = cur.fetchall()
    if user_data:
        session['user'] = user_data[0][0]
        return redirect(url_for('userDashboard'))
    return render_template('login.html', message = "Invalid credentials. Please try again.")

@app.route('/userdashboard')
def userDashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('userdashboard.html', user = session['user'])

@app.route('/merchant')
def merchant():
    return render_template('merchantregister.html')

@app.route('/merchant_register', methods=["GET", "POST"])
def merRegister():
    mer_name = request.form['mer_name']
    mer_email = request.form['mer_email']
    mer_pwd = request.form['pwd']
    mer_tax_rate = request.form['tax_rate']

    try:
        query = "INSERT INTO merchants(mer_name, mer_email, merchant_pwd, mer_tax_rate) VALUES (%s, %s, %s, %s)"
        values = (mer_name, mer_email, mer_pwd, mer_tax_rate)
        cur.execute(query, values)
        mydb.commit()
        return render_template('register_success.html', message="Registration Successful! Thank you for registering.")
    except:
        return render_template('register_success.html', message="Failed while registering. Please try again.")

@app.route('/merchant_login', methods=["POST", "GET"])
def merLogin():
    u_email = request.form['mer_email']
    u_pwd = request.form['mer_pwd']
    cur.execute("SELECT * FROM merchants WHERE mer_email=%s AND merchant_pwd=%s", (u_email, u_pwd))
    data = cur.fetchall()
    if data:
        session['merchant'] = data[0]
        return redirect(url_for('merchantDashboard'))
    return render_template('login.html', message="Invalid credentials. Please try again.")

@app.route('/merchantdashboard')
def merchantDashboard():
    if 'merchant' not in session:
        return redirect(url_for('index'))
    return render_template('merchantdashboard.html', merchant=session['merchant'])

@app.route('/add_product', methods=["GET", "POST"])
def addProduct():
    if request.method == "POST":
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        price = float(request.form['price'])
        app = request.form['app']

        try:
            query = "INSERT INTO products(product_id, product_name, price, app) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (product_id, product_name, price, app))
            mydb.commit()
            return render_template('product_success.html', message="Product added successfully.")
        except:
            return render_template('product_success.html', message="Failed to add product. Please try again.")
    return render_template('add_product.html')

@app.route('/confirm_payment', methods=["POST"])
def purchaseProduct():
    product_id = request.form['product_id']
    product_name = request.form['product_name']
    price = float(request.form['price'])

    if 'user' not in session:
        return redirect(url_for('index'))

    user_name = session['user']
    query = "SELECT user_credit FROM users WHERE user_name=%s"
    cur.execute(query, (user_name,))
    user_credit = cur.fetchone()[0]

    if float(user_credit) >= price:
        try:
            update_query = "UPDATE users SET user_credit = user_credit - %s WHERE user_name = %s"
            cur.execute(update_query, (price, user_name))
            mydb.commit()
            return render_template('ordersuccessful.html', message="Payment successful! Thank you for your purchase.")
        except:
            return render_template('ordersuccessful.html', message="Transaction failed. Please try again.")
    else:
        return render_template('payment_failure.html', message="Insufficient credit. Please add more credit to proceed.")

if __name__ == '__main__':
    app.run(debug=True)
