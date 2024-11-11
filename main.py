#Import Libraries
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Create Flask App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///restaurant_pos.db'
db = SQLAlchemy(app)

#Initialize Relationship Schema
#Order Schema
class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)                                #Add Auto Increment
    cust_id = db.Column(db.Integer, db.ForeignKey("customer.cust_id"))         #References cust_id in customer? #Update: I think this is the right way
    table_id = db.Column(db.Integer)                                                  #References table_id in table?
    order_time = db.Column(db.DateTime, default = datetime.today(), nullable=False)   #idk if this is the right datetime function, will change later
    total_cost = db.Column(db.Integer, nullable=False)                                #add logic for incrementing later, change to decimal

#Customer Schema
class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True)                                 #Add Auto Increment
    cust_first_name = db.Column(db.String(50), nullable=False)                  
    cust_last_name = db.Column(db.String(50), nullable=False)
    phone_no = db.Column(db.String(10), nullable=False)                               #How to make unique?
    Email = db.Column(db.String(60), nullable=False)                                  #How to make unique?
    pref_table = db.Column(db.Integer)                                                #References table_id in table?

#Table Schema
class Table(db.Model):
    table_id = db.Column(db.Integer, primary_key=True, nullable=False)                                  #How to make unique?
    capacity = db.Column(db.Integer, nullable=False)                                  #How to make unique?
    loc = db.Column(db.String(20))

#Reservation Schema
class Reservation(db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)                          #Add auto increment
    cust_id = db.Column(db.Integer, nullable=False)                                   #Add foreign key
    date_created = db.Column(db.DateTime, default = datetime.today(), nullable=False) #idk if this is the right datetime function, will change later
    date_reserved = db.Column(db.DateTime, default = datetime.today(), nullable=False)#pulls current time, find function to pull select time

#Payment Schema
class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True, nullable=False)              #Add auto increment
    order_id = db.Column(db.Integer, nullable=False)                                  #Add Foreign Key
    amount = db.Column(db.Integer, nullable=False)                                    #Change to decimal
    payment_method = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, default = datetime.today(), nullable=False)

#MenuCategory Schema
class MenuCat(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, nullable=False)                               #increments
    name = db.Column(db.String(30), nullable=False)                                   #Unique?

#MenuItem Schema
class MenuItem(db.Model):
    menu_item_id = db.Column(db.Integer, primary_key=True, nullable=False)                              #Increments
    category_id = db.Column(db.Integer, nullable=False)                               #References cat_id in MenuCategory
    name = db.Column(db.String(50), nullable=False)                                   #Unique?
    desc = db.Column(db.String(200))
    price = db.Column(db.Integer, nullable=False)                                     #Change to decimal

#OrderItem Schema
class OrderItem(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True)                                            #Increments
    order_id = db.Column(db.Integer, nullable=False)                                 #references order_id in Order
    menu_item_id = db.Column(db.Integer, nullable=False)                             #references menu_item_id in MenuItem
    quantity = db.Column(db.Integer, nullable=False)
    special_instructions = db.Column(db.String(100))

#Create Database, run once then comment out when db is created
# with app.app_context():
#    db.create_all()

#Code to write to the App
#Open App
#These are the old functions, we need to entirely gut these for our own purposes 
# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']

#         new_task = Todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'
        
#     else:
#        tasks = Todo.query.order_by(Todo.date_created).all()
#        return render_template('index.html',tasks=tasks)

# #Delete Content
# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task'

# #Update Site 
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)
#     if request.method == 'POST':
#         task.content = request.form['content']
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#                return 'There was an issue updating your task'
#     else:
#         return render_template('update.html', task=task)


# if __name__ == '__main__':
#     app.run(debug=True)
    
