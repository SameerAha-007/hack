from flask import Flask, render_template, request, session
import mysql.connector as db


mydb = db.connect(host = 'localhost', user = 'root', password = "Mahesh@123", db = 'hackathon')

cur = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def user():
    if(session['user']):
        return render_template('login.html')
    else:
        return render_template('userdashboard.html')
    

@app.route('/user_register', methods = ["GET", "POST"])
def userRegister():
    user_name = request.form['u_name']
    user_email = request.form['u_email']
    user_phone = request.form['phone']
    user_address = request.form['u_address']
    user_credit = request.form['credit']
    user_pwd = request.form['u_pwd']
    
    try:
        cur.execute(f"insert into users values(%s, %s, %s, %s, %s, %s)",(user_name, user_email, user_phone, user_address, user_credit, user_pwd))
        mydb.commit()
        return render_template('register_success.html',message = "Registeration Succesfull!, Thank for Registering")
    

    except:
        return render_template('register_success.html', message = "Failed While Registring, Retry Agian")
    
@app.route('/user_login', methods = ["POST", "GET"])
def userLogin():
    if(session['user']):
        return render_template('userdashboard.html')
    else:
        u_email = request.form['u_email']
        u_pwd = request.form['pwd']

        try:
            cur.execute(f'select * from users where user_email={u_email}')
            user_data = cur.fetchall()
            if(user_data[5] == u_pwd):
                session['user'] = user_data[0]
                return render_template('userdashboard.html')
            else:
                return render_template('login.html', login_error = "Invalid password")
        except:
            return render_template('login.html', login_error = "Login Failed!, User Not Exists with the given email")


    

@app.route('/merchant')
def merchant():
    if(session['merchant']):
        return render_template('login.html')
    else:
        return render_template('userdashboard.html')
    
@app.route('/merchant_register', methods = ["GET", "POST"])
def userRegister():
    mer_name = request.form['mer_name']
    mer_email = request.form['mer_email']
    mer_pwd = request.form['pwd']
    mer_tax_rate = request.form['tax_rate']
    
    try:
        cur.execute(f"insert into merchants values(%s, %s, %s, %s)",(mer_name, mer_email, mer_pwd, mer_tax_rate))
        mydb.commit()
        return render_template('register_success.html',message = "Registeration Succesfull!, Thank for Registering")
    

    except:
        return render_template('register_success.html', message = "Failed While Registring, Retry Agian")
    
@app.route('/merchant_login', methods = ["POST", "GET"])
def userLogin():
    if(session['merchant']):
        return render_template('merchantdashboard.html')
    else:
        u_email = request.form['u_email']
        u_pwd = request.form['pwd']

        try:
            cur.execute(f'select * from merchants where mer_email={u_email}')
            user_data = cur.fetchall()
            if(user_data[2] == u_pwd):
                session['merchant'] = user_data[0]
                return render_template('merchantdashboard.html')
            else:
                return render_template('login.html', login_error = "Invalid password")
        except:
            return render_template('login.html', login_error = "Login Failed!, User Not Exists with the given email")


@app.route('/confirmpayment')
def confirmPayment():
    return render_template('order_successful.html')

@app.route('/userdashboard')
def userDashboard():
    return render_template('userdashboard')


@app.route('/merchantdashboard')
def merchantDashboard():
    return render_template('merchantdashboard.html')

app.run(debug=True)