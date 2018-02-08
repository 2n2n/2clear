#core dependencies
import os
from flask import Flask, abort, flash, redirect, render_template, request,session, make_response, jsonify
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy import update

#models and libs
from models.CustomerModel import CustomerModel
from models.User import User
from models.Stock import Stock
from models.Products import Products
from datetime import datetime

#blueprints
from apps.sampleBlueprint import sample

# all resources
from resources.Customer import CustomerRegister, CustomerData
from resources.User import UserRegister
from resources.Products import Registerproducts
from resources.stocks import UpdateStocks
from resources.stocks import getBydate
from resources.Products import getprice

app = Flask(__name__)
dbname   = 'mysql+pymysql://root:@127.0.0.1/2_clear'

CORS(app, supports_credentials=True, resources={r"*": {"origins": "*"}})


app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', dbname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(12)

api = Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(jsonify(data), code)
    resp.headers.extend(headers or {})
    return resp


@app.route('/')
def home():
    users = User.query.all()    

    customers = CustomerModel.query.all() 
    if session.get('logged_in'):
        return render_template('home.html', customers=customers,users=users)
    else:
        return render_template('login.html', users=users,customers=customers)


    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('login.html', users=users)
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])


    query = User.query.filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()

    if result:
        session['uid'] = result.id
        session['logged_in'] = True
        session['username'] = result.username
        session['name'] = result.name
        session['role'] =result.role
        # redirect to /home
    else:
        flash('wrong password!')
        # redirect to login
    return redirect('/')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')


@app.route("/transactions")
def transactions():
    customers = CustomerModel.query.all()
    products = Products.query.all()
    session['logged_in'] = True 
    return render_template('transactions.html',products=products,customers=customers)

@app.route("/viewcustomers")
def viewcustomers():
    customers = CustomerModel.query.all()
    products = Products.query.all()
    session['logged_in'] = True 
    return render_template('viewcustomers.html',products=products,customers=customers)

@app.route("/registrations")
def registrations():
    return render_template('adduser.html')

@app.route("/admin")
def admin():
  
    return render_template('adminpanel.html')



@app.route("/vieworders")
def vieworders():
    return render_template('Orders.html')

@app.route("/reports")
def reports():
    #stocks= Stock.query.all()
    #return render_template('reports.html',stocks=stocks)
    qdate = request.form['sdate']
    qry = Stock.query(Stock.date).filter(Stock.date.where(qdate))
    
    return render_template('reports.html',qry=qry)

@app.route("/reportsout")
def reportsout():
    stocks= Stock.query.all()
    return render_template('reportstockout.html',stocks=stocks)


#@app.route("/search_by_date")
#def search_by_date():
#    datediss = Stock.query.filter_by(date=valuedate)
#    return datediss
    
     # return render_template('reports.html', filteredstocks=filteredstocks)

@app.route("/aproduct")
def adminproduct():
    return render_template('adminproducts.html')

@app.route("/aadd")
def aadd(): 

    return render_template('adminadduser.html')

@app.route("/amanage")
def amanage(): 
    users = User.query.all()
    return render_template('adminaccounts.html')

#@app.route("/aastock")
#def astock():
#
#    products = Products.query.all()
#    POST_AMOUNT = request.form['amount']
#    Products.update().values(quantity=POST_AMOUNT).where(
#        Product.name
#    )

#    return render_template('adminstockin.html', products=products)


#@app.route("/aastock/<int:_id>", methods=['POST','GET'])
#def aastock(_product):
#    return _product
#    POST_AMOUNT = request.form['amount']
#    return products.json()
#    products.quantity = str(products.quantity) + POST_AMOUNT
#    products.insert()
#    return render_template('reports.html')

@app.route("/products")
def products():
    stocks = Stock.query.all()
    products = Products.query.all()
    
    return render_template('products.html',stocks=stocks, products=products )



@app.route("/return")
def returnn():
 
    return render_template('return.html')

@app.route("/recordnewcustomer",  methods=['POST'])
def recordnewcustomer():
    users = User.query.all()

    POST_CNAME = request.form['customername']
    POST_CADDRESS = request.form['customeraddress']
    POST_CCONTACT = request.form['customercontact']

    new_customer = CustomerModel(
        name = POST_CNAME,
        address = POST_CADDRESS,
        number = POST_CCONTACT
    )
    new_customer.insert()

    customers = CustomerModel.query.all()

    return render_template('adduser.html', customers=customers,users=users)

@app.route('/recordnewuser', methods=['POST'])
def recordnewuser():     

    POST_USERNAME = str(request.form['username'])
    POST_NAME = str(request.form['user_name'])
    POST_PASS = str(request.form['password'])
    POST_CPASS = str(request.form['confirmpassword'])
    POST_ROLE = str(request.form['role'])

    new_user = User(
        username = POST_USERNAME,
        password = POST_PASS,
        name = POST_NAME,
        role = POST_ROLE
    )
    try:
        new_user.insert()
        return render_template('adduser.html', customers=customers,users=users)
    except:
        return 'error'

@app.route('/Registerproduct', methods=['POST'])
def Registerproduct():     

    POST_PRODNAME = str(request.form['productname'])
    POST_PRODPRICE = str(request.form['sp'])
    POST_PRODQUANTITY = str(request.form['quantity'])
    POST_PRODTYPE = str(request.form['type'])
    new_product = Product(
        pname = POST_PRODNAME,
        pprice = POST_PRODPRICE,
        quantity = POST_PRODQUANTITY,
        ptype = POST_PRODTYPE
    )
    try:
        new_user.insert()
        return render_template('adminproducts.html')
    except:
        return 'error'



#api routes
api.add_resource(CustomerRegister, '/Customer/add')
api.add_resource(UserRegister, '/User/add')
api.add_resource(Registerproducts, '/Products/add')
api.add_resource(UpdateStocks, '/update/stocks')
api.add_resource(CustomerData, '/customer/<int:_id>')
api.add_resource(getprice, '/price/<int:_id>')
api.add_resource(getBydate,'/date/str:_date')

#register blueprints here
app.register_blueprint(sample, url_prefix='/sample')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=4000)
