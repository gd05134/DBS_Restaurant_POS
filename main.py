#Import Libraries
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Create Flask App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///restaurant_pos.db'
db = SQLAlchemy(app)
app.secret_key ='key'

#Initialize Relationship Schema
#Order Schema
class Order(db.Model):                                                     
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    table_id = db.Column(db.Integer, db.ForeignKey("table.table_id"))                                                  
    order_time = db.Column(db.DateTime, default = datetime.now(), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

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
    cust_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_first_name = db.Column(db.String(50), nullable=False)                  
    cust_last_name = db.Column(db.String(50), nullable=False)
    phone_no = db.Column(db.String(10), unique=True, nullable=False)                               
    email = db.Column(db.String(60), unique=True, nullable=False)                                
    pref_table = db.Column(db.Integer, db.ForeignKey("table.table_id")) 
    date_created = db.Column(db.DateTime, default = datetime.now(), nullable=False) 
    date_reserved = db.Column(db.DateTime, default = datetime.now(), nullable=False)             

    def __init__(self, cust_first_name, cust_last_name, phone_no, email, pref_table):
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


#Payment Schema
class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    order_id = db.Column(db.Integer,db.ForeignKey("order.order_id"), nullable=False)        
    amount = db.Column(db.Float, nullable=False)                                            
    payment_method = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, default = datetime.today(), nullable=False)

    def __init__(self, order_id, amount, payment_method):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method

#MenuCategory Schema
class MenuCat(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)                                  

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'<MenuCat {self.name}>'

#MenuItem Schema
class MenuItem(db.Model): 
    menu_item_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey("menu_cat.category_id"), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)                              
    price = db.Column(db.Float, nullable=False)                                               

    def __init__(self, category_id, name, price):
        self.category_id = category_id
        self.name = name
        self.price = price
        
#OrderItem Schema
class OrderItem(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer,db.ForeignKey("order.order_id"), nullable=False)
    menu_item_id = db.Column(db.Integer,db.ForeignKey("menu_item.menu_item_id"), nullable=False)                         
    quantity = db.Column(db.Integer, nullable=False)
    special_instructions = db.Column(db.String(100))

    menu_item = db.relationship('MenuItem', backref='order_items')                     

    menu_item_id = db.Column(db.Integer,db.ForeignKey("menu_item.menu_item_id"), nullable=False)                         
    def __init__(self, order_id, menu_item_id, quantity, special_instructions):
        self.order_id = order_id
        self.menu_item_id = menu_item_id
        self.quantity = quantity
        self.special_instructions = special_instructions

# # Adding Customers (Run Once - Don
# with app.app_context():
#     # customers = db.session.query(Customer).join(Reservation).filter(Reservation.cust_id == Customer.cust_id).all()
#     # reservations = Reservation.query.order_by(Reservation.reservation_id).all()
#     # print(customers)
#     # print(reservations)  
#     db.create_all()
#     #add menu item and menu categories
#     #For testing, only run once    
#     db.session.add(Customer("Caelin","Jones","3679807695","cj20948@georgiasouthern.edu", 5))
#     db.session.add(Customer("Garth","Daniels","9124673847","gd05134@georgiasouthern.edu",10))
#     db.session.add(Customer("Grey","Myers","5065971493","gm08348@georgiasouthern.edu",2))
#     db.session.add(Customer("Tong","Weitian","33333333","wtong@georgiasouthern.edu",10))
#     for i in range(1,11):
#         db.session.add(Table(i, 4, "Our Restaurant"))
#     db.session.commit()

# # Adding Menu Items (Run Once - Done)
# with app.app_context():
#     # Clear
#     db.session.query(MenuCat).delete()
#     db.session.query(MenuItem).delete()
#     db.session.commit()
  
#     db.create_all()
#     db.session.add(MenuCat(name="Drinks"))
#     db.session.add(MenuCat(name="Appetizers"))
#     db.session.add(MenuCat(name="Pastas"))
#     db.session.add(MenuCat(name="Pizzas"))
#     db.session.add(MenuCat(name="Sandwiches"))
#     db.session.add(MenuCat(name="Specialties"))
#     db.session.add(MenuCat(name="Kids"))
#     db.session.add(MenuCat(name="Add-Ons"))
#     db.session.add(MenuCat(name="Desserts"))

#     # Drinks
#     db.session.add(MenuItem(category_id=1, name="Coke", price=2.50))
#     db.session.add(MenuItem(category_id=1, name="Coke Zero", price=2.50))
#     db.session.add(MenuItem(category_id=1, name="Diet Coke", price=2.50))
#     db.session.add(MenuItem(category_id=1, name="Sprite", price=2.50))
#     db.session.add(MenuItem(category_id=1, name="Barqs", price=2.50))
#     db.session.add(MenuItem(category_id=1, name="Dr. Pep", price=2.50))
#     db.session.add(MenuItem(category_id=1, name="Fanta", price=2.50))
#     db.session.add(MenuItem(category_id=1, name="Rspbry. Ital. Soda", price=3.50))
#     db.session.add(MenuItem(category_id=1, name="Orange Ital. Soda", price=3.50))
#     db.session.add(MenuItem(category_id=1, name="Lemon Ital. Soda", price=3.50))
#     db.session.add(MenuItem(category_id=1, name="Sparkling Water", price=3.50))
#     db.session.add(MenuItem(category_id=1, name="Water", price=0.00))
    
#     # Appetizers
#     db.session.add(MenuItem(category_id=2, name="Bruschetta al Pomodoro", price=9.00))
#     db.session.add(MenuItem(category_id=2, name="Mozzarella Balls", price=7.00))
#     db.session.add(MenuItem(category_id=2, name="Caprese Salad", price=8.00))
#     db.session.add(MenuItem(category_id=2, name="Garlic Knots", price=6.50))
#     db.session.add(MenuItem(category_id=2, name="Baked Goat Cheese Dip", price=9.00))
#     db.session.add(MenuItem(category_id=2, name="Focaccia Bread", price=6.00))
#     db.session.add(MenuItem(category_id=2, name="Antipasto Skewers", price=8.50))
    
#     # Pastas
#     db.session.add(MenuItem(category_id=3, name="Spaghetti Carbonara", price=16.00))
#     db.session.add(MenuItem(category_id=3, name="Fettuccine Alfredo", price=14.00))
#     db.session.add(MenuItem(category_id=3, name="Penne Arrabbiata", price=13.50))
#     db.session.add(MenuItem(category_id=3, name="Lasagna Bolognese", price=16.00))
#     db.session.add(MenuItem(category_id=3, name="Spaghetti All'ubriaco", price=15.00))
#     db.session.add(MenuItem(category_id=3, name="Linguine with Clams", price=17.50))
#     db.session.add(MenuItem(category_id=3, name="Penne alla Norma", price=14.00))
    
#     # Pizzas
#     db.session.add(MenuItem(category_id=4, name="Pepperoni and Mushroom (S)", price=13.00))
#     db.session.add(MenuItem(category_id=4, name="Pepperoni and Mushroom (L)", price=16.00))
#     db.session.add(MenuItem(category_id=4, name="Margherita (S)", price=13.00))
#     db.session.add(MenuItem(category_id=4, name="Margherita (L)", price=16.00))
#     db.session.add(MenuItem(category_id=4, name="Quattro Stagioni (S)", price=15.00))
#     db.session.add(MenuItem(category_id=4, name="Quattro Stagioni (L)", price=18.00))
#     db.session.add(MenuItem(category_id=4, name="Prosciutto e Rucola (S)", price=15.00))
#     db.session.add(MenuItem(category_id=4, name="Prosciutto e Rucola (L)", price=18.00))
    
#     # Sandwiches
#     db.session.add(MenuItem(category_id=5, name="Chicken Parmesan Sub", price=10.50))
#     db.session.add(MenuItem(category_id=5, name="Italian Meatball", price=11.50))
#     db.session.add(MenuItem(category_id=5, name="Caprese Panini", price=10.00))
#     db.session.add(MenuItem(category_id=5, name="Prosciutto and Provolone", price=13.00))
#     db.session.add(MenuItem(category_id=5, name="Lampredotto Panino", price=14.00))
    
#     # Specialties
#     db.session.add(MenuItem(category_id=6, name="Chicken Marsala", price=17.50))
#     db.session.add(MenuItem(category_id=6, name="Veal Piccata", price=20.00))
#     db.session.add(MenuItem(category_id=6, name="Eggplant Parmesan", price=16.00))
#     db.session.add(MenuItem(category_id=6, name="Osso Buco", price=24.00))
    
#     # Kids
#     db.session.add(MenuItem(category_id=7, name="Cheese Pizza", price=8.00))
#     db.session.add(MenuItem(category_id=7, name="Meatball Sub", price=8.00))
#     db.session.add(MenuItem(category_id=7, name="Grilled Cheese & Tomato Soup", price=5.00))
#     db.session.add(MenuItem(category_id=7, name="Dino Nuggies", price=5.00))
#     db.session.add(MenuItem(category_id=7, name="Chocolate Milk", price=3.00))
    
#     # Add-Ons
#     db.session.add(MenuItem(category_id=8, name="A Plate of Meatballs", price=5.00))
#     db.session.add(MenuItem(category_id=8, name="A Whole Raw Eggplant", price=3.00))
#     db.session.add(MenuItem(category_id=8, name="Breadsticks To Go", price=2.00))

#     # Desserts
#     db.session.add(MenuItem(category_id=9, name="Tiramisu ", price=8.50))
#     db.session.add(MenuItem(category_id=9, name="Cannoli ", price=6.50))
#     db.session.add(MenuItem(category_id=9, name="Panna Cotta", price=7.00))
#     db.session.add(MenuItem(category_id=9, name="Gelato Flight", price=9.50))
    
#     db.session.commit()

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
        customers = Customer.query.order_by(Customer.cust_id).all()
        return render_template('reservation_manager.html', customers = customers)

@app.route('/menu', methods=['GET', 'POST'])
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
        
        order_id = request.args.get('order_id')
        order_items = []
        
        if order_id:
            order_items = (
                db.session.query(
                    OrderItem.menu_item_id,
                    MenuItem.name,
                    OrderItem.quantity,
                    MenuItem.price
                )
                .join(MenuItem, OrderItem.menu_item_id == MenuItem.menu_item_id)
                .filter(OrderItem.order_id == order_id)
                .all()
            )

        order_items_data = [{
            'name': item.name,
            'quantity': item.quantity,
            'price': item.price,
            'item_id': item.menu_item_id
        } for item in order_items]
        
        return render_template('menu.html', 
                               categories=categories, 
                               table=table,
                               order_items=order_items_data)

@app.route('/menu_items/<int:category_id>')
def menu_items(category_id):
    items = MenuItem.query.filter_by(category_id=category_id).all()
    items_data = [{'name': item.name, 'price': item.price, 'item_id':item.menu_item_id} for item in items]
    return jsonify(items_data)

@app.route('/payment/<int:table_id>', methods=['GET','POST'])
def payment(table_id):
     if request.method == 'POST':
        order_id = request.form['order_no']
        payment_method = request.form['payment_manager']
        
        order = Order.query.filter_by(order_id=order_id, table_id=table_id).first()
        if not order:
            flash(f"Input Order ID ({order_id}) is not associated with the current table ({table_id}).", "error")
            return redirect(f'/payment/{table_id}')
        
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

    
@app.route('/submit_order', methods=['POST'])
def submit_order():
    order_data = request.get_json()
    table_id = order_data['table_id']
    order_items = order_data['order_items']
    total_cost = order_data['total_cost']
    order_id = order_data.get('order_id')

    if order_id:
        order = Order.query.get(order_id)
        if order:
            order.total_cost = total_cost
            db.session.commit()

            OrderItem.query.filter_by(order_id=order_id).delete()
            db.session.commit()

            for item in order_items:
                order_item = OrderItem(order_id=order.order_id, menu_item_id=item["item_id"], 
                                       quantity=item['quantity'], special_instructions="")
                db.session.add(order_item)

            db.session.commit()
        else:
            return jsonify({"success": False, "message": "Order not found."})

    else:
        new_order = Order(table_id=table_id, order_time=datetime.now(), total_cost=total_cost)
        db.session.add(new_order)
        db.session.commit()

        for item in order_items:
            order_item = OrderItem(order_id=new_order.order_id, menu_item_id=item["item_id"], 
                                quantity=item['quantity'], special_instructions="")
            db.session.add(order_item)

        db.session.commit()

    return jsonify({"success": True})



@app.route('/get_order_items/<int:order_id>')
def get_order_items(order_id):
    order_items = (
        db.session.query(
            OrderItem.menu_item_id,
            MenuItem.name,
            OrderItem.quantity,
            MenuItem.price
        )
        .join(MenuItem, OrderItem.menu_item_id == MenuItem.menu_item_id)
        .filter(OrderItem.order_id == order_id)
        .all()
    )

    order_items_data = [{
        'name': item.name,
        'quantity': item.quantity,
        'price': item.price,
        'item_id': item.menu_item_id
    } for item in order_items]

    return jsonify(order_items_data)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(directory='.', path='favicon.ico', mimetype='image/vnd.microsoft.icon')



if __name__ == '__main__':
     app.run(debug=True)