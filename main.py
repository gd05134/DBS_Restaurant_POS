#Import Libraries
from flask import render_template, url_for, request, redirect, flash, jsonify, send_from_directory
from datetime import datetime

from database_classes import app, db, Order, Customer, Table, Payment, MenuCat, MenuItem, OrderItem

#Create Flask App

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

#Search Manager Layout
@app.route('/search_manager', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        try:
            db.session.commit()
            return redirect('/search_manager')
        except:
               return 'There was an issue opening the order'
    else:
        return render_template('search_manager.html')

if __name__ == '__main__':
     app.run(debug=True)