#Import Libraries
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#global variables if needed

#Create Flask App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///restaurant_pos.db'
db = SQLAlchemy(app)
app.secret_key ='key'

#Initialize Relationship Schema
#Order Schema
class Order(db.Model):                                                              #* GAD - Removed cust_id from Orders
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)          #* GAD - Added auto-increment     
    table_id = db.Column(db.Integer, db.ForeignKey("table.table_id"))                                                  
    order_time = db.Column(db.DateTime, default = datetime.now(), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)                              #add logic for incrementing later  #? Is this still needed?
                                                                                  #* GAD - Changed to float

    order_items = db.relationship(
        'OrderItem',
        cascade="all, delete-orphan",
        backref='order'
    )

    def __init__(self, table_id, order_time, total_cost):
        self.table_id = table_id
        self.order_time = order_time
        self.total_cost = total_cost

#Customer Schema
class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True, autoincrement=True)       #* GAD - Added auto-increment
    cust_first_name = db.Column(db.String(50), nullable=False)                  
    cust_last_name = db.Column(db.String(50), nullable=False)
    phone_no = db.Column(db.String(10), unique=True, nullable=False)                               
    email = db.Column(db.String(60), unique=True, nullable=False)                                
    pref_table = db.Column(db.Integer, db.ForeignKey("table.table_id")) 
    date_created = db.Column(db.DateTime, default = datetime.now(), nullable=False) 
    date_reserved = db.Column(db.DateTime, default = datetime.now(), nullable=False)             

    def __init__(self, cust_first_name, cust_last_name, phone_no, email, pref_table):
        #self.cust_id = cust_id                                                 #* GAD - Removed auto-incrementing ID from __init__
        self.cust_first_name = cust_first_name
        self.cust_last_name = cust_last_name
        self.phone_no = phone_no
        self.email = email
        self.pref_table = pref_table

#Table Schema
class Table(db.Model):
    table_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)                                  
    capacity = db.Column(db.Integer, nullable=False)                                 
    loc = db.Column(db.String(20))
    
    def __init__(self, table_id, capacity, loc):
        self.table_id = table_id
        self.capacity = capacity
        self.loc = loc

#Reservation Schema                                                                                #! REMOVED RESERVATION TABLE
# class Reservation(db.Model):
#     reservation_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)     #* GAD - Added auto-increment
#     cust_id = db.Column(db.Integer, db.ForeignKey("customer.cust_id"), nullable=False)                        
#     date_created = db.Column(db.DateTime, default = datetime.now(), nullable=False) 
#     date_reserved = db.Column(db.DateTime, default = datetime.now(), nullable=False)              #todo: pulls current time, find function to pull select time

#     def __init__(self, cust_id):
#         #self.reservation_id = reservation_id                                           #* GAD - Removed auto-incrementing ID from __init__
#         self.cust_id = cust_id

#Payment Schema
class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)    #* GAD - Added auto-increment
    order_id = db.Column(db.Integer,db.ForeignKey("order.order_id"), nullable=False)                                 
    amount = db.Column(db.Float, nullable=False)                                                #* GAD - Changed to Float
    payment_method = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, default = datetime.today(), nullable=False)

    def __init__(self, order_id, amount, payment_method):
        #self.payment_id = payment_id                                                           #* GAD - Removed auto-incrementing ID from __init__
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method

#MenuCategory Schema
class MenuCat(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)    #* GAD - Added auto-increment
    name = db.Column(db.String(30), unique=True, nullable=False)                                  

    def __init__(self, name):
        #self.category_id = category_id                                                          #* GAD - Removed auto-incrementing ID from __init__
        self.name = name
    
    def __repr__(self):
        return f'<MenuCat {self.name}>'

#MenuItem Schema
class MenuItem(db.Model): 
    menu_item_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)   #* GAD - Added auto-increment
    category_id = db.Column(db.Integer, db.ForeignKey("menu_cat.category_id"), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)                                #* GAD - Removed "Description"
    price = db.Column(db.Float, nullable=False)                                                 #* GAD - Changed to Float

    def __init__(self, category_id, name, price):
        #self.menu_item_id = menu_item_id                                                       #* GAD - Removed auto-incrementing ID from __init__
        self.category_id = category_id
        self.name = name
        self.price = price
        
#OrderItem Schema
class OrderItem(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)        #* GAD - Added auto-increment
    order_id = db.Column(db.Integer,db.ForeignKey("order.order_id"), nullable=False)
    # order = db.relationship('Order', backref='order_items')                            #! MOVED TO ORDER CBJ
    menu_item_id = db.Column(db.Integer,db.ForeignKey("menu_item.menu_item_id"), nullable=False)                         
    quantity = db.Column(db.Integer, nullable=False)
    special_instructions = db.Column(db.String(100))

    menu_item = db.relationship('MenuItem',                                            #* GAD - Added Database Relationship
                                backref='order_items')                     

    menu_item_id = db.Column(db.Integer,db.ForeignKey("menu_item.menu_item_id"), nullable=False)                         
    def __init__(self, order_id, menu_item_id, quantity, special_instructions):
        #self.order_item_id = order_item_id                                            #* GAD - Removed auto-incrementing ID from __init__
        self.order_id = order_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity
        self.special_instructions = special_instructions

#Main Restaurant Layout
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            
            db.session.commit()
            return redirect('/')
        except:
               return 'There was an issue opening the order'
    else:
        return render_template('index.html')

#To enter Order state
@app.route('/order_manager/<int:table_id>', methods=['GET', 'POST'])
def order(table_id):
     table = Table.query.get_or_404(table_id)
     if request.method == 'POST':
        try:
            db.session.commit()
            return redirect(url_for('/order_manager/'))
        except:
               return 'There was an issue opening the layout'
     else:                 
        orders = (
            db.session.query(
                Order.order_id,
                Order.order_time,
                Order.total_cost,
                db.func.group_concat(MenuItem.name, ", ").label("food_items"),
                db.func.group_concat(OrderItem.quantity, ", ").label("food_quantities")
            )
            .join(OrderItem, Order.order_id == OrderItem.order_id)
            .join(MenuItem, OrderItem.menu_item_id == MenuItem.menu_item_id)
            .filter(Order.table_id == table_id)
            .group_by(Order.order_id)
            .order_by(Order.order_time)
            .all()
        )
        
        processed_orders = []
        for order in orders:
            food_item_list = (order.food_items).split(',')
            food_quantities_list = (order.food_quantities).replace(' ','').split(',')
            food_items = []
            for i in range(0, len(food_item_list)):
                food_items.append(f"{food_item_list[i]} (x{food_quantities_list[i]})")
            processed_orders.append({
                'order_id': order.order_id,
                'order_time': (order.order_time).strftime("%m/%d/%Y %H:%M:%S"),
                'food_list': '\n'.join(food_items),
                'total_cost': order.total_cost
            })
        
        return render_template('order_manager.html', table = table, orders = processed_orders)

#For reservations
@app.route('/reservation_manager', methods=['GET','POST'])
def add_reservation():
    if request.method == 'POST':
        cust_first_name = request.form['First Name']
        cust_last_name = request.form['Last Name']
        phone_no = request.form['Phone No.']
        email = request.form['Email']
        pref_table = request.form['Preferred Table']
        try:
            db.session.add(Customer(cust_first_name, 
                                    cust_last_name, 
                                    phone_no, email, 
                                    pref_table))
            db.session.commit()
            return redirect('/reservation_manager')
        except:
            return 'There was an issue reserving your table'
    else:
        # reservations = Reservation.query.order_by(Reservation.reservation_id).all()
        customers = Customer.query.order_by(Customer.cust_id).all()
        # customers = db.session.query(Customer).join(Reservation, Reservation.cust_id == Customer.cust_id).all()
        return render_template('reservation_manager.html', customers = customers)

@app.route('/menu', methods=['GET', 'POST']) # GAD
def menu():
    if request.method == 'POST':
        try:
            db.session.commit()
            return redirect('/menu')
        except:
            return 'There was an issue opening the menu'
    else:
        categories = MenuCat.query.all()
        table = Table.query.first()
        return render_template('menu.html', categories=categories, table=table)

@app.route('/menu_items/<int:category_id>') # GAD
def menu_items(category_id):
    items = MenuItem.query.filter_by(category_id=category_id).all()
    items_data = [{'name': item.name, 'price': item.price, 'item_id':item.menu_item_id} for item in items]
    return jsonify(items_data)
     
@app.route('/payment/<int:table_id>', methods=['GET','POST'])
def payment(table_id):
     if request.method == 'POST':
        order_id = request.form['order_no']
        payment_method = request.form['payment_manager']
        order_to_delete = Order.query.get_or_404(order_id)
        try:
            db.session.add(Payment(order_id, order_to_delete.total_cost, payment_method))
            db.session.delete(order_to_delete)
            db.session.commit()
            return redirect(f'/payment/{table_id}')
        except:
               return 'There was an issue opening the menu'
     else:
        orders_at_table = db.session.query(Order).join(Table, Order.table_id == table_id).all()
        payments = Payment.query.order_by(Payment.payment_id).all()
        return render_template('payment_manager.html',
                               table_id = table_id, 
                               payments = payments, 
                               orders_at_table = orders_at_table)
    
@app.route('/submit_order', methods=['POST']) # GAD
def submit_order():
    order_data = request.get_json()
    table_id = order_data['table_id']
    order_items = order_data['order_items']
    total_cost = order_data['total_cost']

    new_order = Order(table_id=table_id, order_time=datetime.now(), total_cost=total_cost)
    db.session.add(new_order)
    db.session.commit()

    # Add order items
    for item in order_items:
        order_item = OrderItem(order_id=new_order.order_id, menu_item_id=item["item_id"], 
                               quantity=item['quantity'], special_instructions="")
        db.session.add(order_item)

    db.session.commit()

    return jsonify({"success": True})

if __name__ == '__main__':
     app.run(debug=True)