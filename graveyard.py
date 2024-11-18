# Adding Customers (Run Once - Done)
'''with app.app_context():
    # customers = db.session.query(Customer).join(Reservation).filter(Reservation.cust_id == Customer.cust_id).all()
    # reservations = Reservation.query.order_by(Reservation.reservation_id).all()
    # print(customers)
    # print(reservations)  
    db.create_all()
    #add menu item and menu categories
    #For testing, only run once    db.session.add(Customer(0,"Caelin","Jones","8594892338","jedijones02@gmail.com",7))
    db.session.add(Customer(1,"Garth","Daniels","111111111","mark@gmail.com",4))
    db.session.add(Customer(2,"Grey","Myers","222222222","larryfied@gmail.com",2))
    db.session.add(Customer(3,"Joahna","Ortiz","33333333","wakalover@gmail.com",10))
    for i in range(1,11):
        db.session.add(Table(i, 4, "Our Restaurant"))
    db.session.commit()'''

# Adding Menu Items (Run Once - Done)
'''=with app.app_context():
    # Clear
    db.session.query(MenuCat).delete()
    db.session.query(MenuItem).delete()
    db.session.commit()
  
    db.create_all()
    db.session.add(MenuCat(name="Drinks"))
    db.session.add(MenuCat(name="Appetizers"))
    db.session.add(MenuCat(name="Pastas"))
    db.session.add(MenuCat(name="Pizzas"))
    db.session.add(MenuCat(name="Sandwiches"))
    db.session.add(MenuCat(name="Specialties"))
    db.session.add(MenuCat(name="Kids"))
    db.session.add(MenuCat(name="Add-Ons"))
    db.session.add(MenuCat(name="Desserts"))

    # Drinks
    db.session.add(MenuItem(category_id=1, name="Coke", price=2.50))
    db.session.add(MenuItem(category_id=1, name="Coke Zero", price=2.50))
    db.session.add(MenuItem(category_id=1, name="Diet Coke", price=2.50))
    db.session.add(MenuItem(category_id=1, name="Sprite", price=2.50))
    db.session.add(MenuItem(category_id=1, name="Barqs", price=2.50))
    db.session.add(MenuItem(category_id=1, name="Dr. Pep", price=2.50))
    db.session.add(MenuItem(category_id=1, name="Fanta", price=2.50))
    db.session.add(MenuItem(category_id=1, name="Rspbry. Ital. Soda", price=3.50))
    db.session.add(MenuItem(category_id=1, name="Orange Ital. Soda", price=3.50))
    db.session.add(MenuItem(category_id=1, name="Lemon Ital. Soda", price=3.50))
    db.session.add(MenuItem(category_id=1, name="Sparkling Water", price=3.50))
    db.session.add(MenuItem(category_id=1, name="Water", price=0.00))
    
    # Appetizers
    db.session.add(MenuItem(category_id=2, name="Bruschetta al Pomodoro", price=9.00))
    db.session.add(MenuItem(category_id=2, name="Mozzarella Balls", price=7.00))
    db.session.add(MenuItem(category_id=2, name="Caprese Salad", price=8.00))
    db.session.add(MenuItem(category_id=2, name="Garlic Knots", price=6.50))
    db.session.add(MenuItem(category_id=2, name="Baked Goat Cheese Dip", price=9.00))
    db.session.add(MenuItem(category_id=2, name="Focaccia Bread", price=6.00))
    db.session.add(MenuItem(category_id=2, name="Antipasto Skewers", price=8.50))
    
    # Pastas
    db.session.add(MenuItem(category_id=3, name="Spaghetti Carbonara", price=16.00))
    db.session.add(MenuItem(category_id=3, name="Fettuccine Alfredo", price=14.00))
    db.session.add(MenuItem(category_id=3, name="Penne Arrabbiata", price=13.50))
    db.session.add(MenuItem(category_id=3, name="Lasagna Bolognese", price=16.00))
    db.session.add(MenuItem(category_id=3, name="Spaghetti All'ubriaco", price=15.00))
    db.session.add(MenuItem(category_id=3, name="Linguine with Clams", price=17.50))
    db.session.add(MenuItem(category_id=3, name="Penne alla Norma", price=14.00))
    
    # Pizzas
    db.session.add(MenuItem(category_id=4, name="Pepperoni and Mushroom (S)", price=13.00))
    db.session.add(MenuItem(category_id=4, name="Pepperoni and Mushroom (L)", price=16.00))
    db.session.add(MenuItem(category_id=4, name="Margherita (S)", price=13.00))
    db.session.add(MenuItem(category_id=4, name="Margherita (L)", price=16.00))
    db.session.add(MenuItem(category_id=4, name="Quattro Stagioni (S)", price=15.00))
    db.session.add(MenuItem(category_id=4, name="Quattro Stagioni (L)", price=18.00))
    db.session.add(MenuItem(category_id=4, name="Prosciutto e Rucola (S)", price=15.00))
    db.session.add(MenuItem(category_id=4, name="Prosciutto e Rucola (L)", price=18.00))
    
    # Sandwiches
    db.session.add(MenuItem(category_id=5, name="Chicken Parmesan Sub", price=10.50))
    db.session.add(MenuItem(category_id=5, name="Italian Meatball", price=11.50))
    db.session.add(MenuItem(category_id=5, name="Caprese Panini", price=10.00))
    db.session.add(MenuItem(category_id=5, name="Prosciutto and Provolone", price=13.00))
    db.session.add(MenuItem(category_id=5, name="Lampredotto Panino", price=14.00))
    
    # Specialties
    db.session.add(MenuItem(category_id=6, name="Chicken Marsala", price=17.50))
    db.session.add(MenuItem(category_id=6, name="Veal Piccata", price=20.00))
    db.session.add(MenuItem(category_id=6, name="Eggplant Parmesan", price=16.00))
    db.session.add(MenuItem(category_id=6, name="Osso Buco", price=24.00))
    
    # Kids
    db.session.add(MenuItem(category_id=7, name="Cheese Pizza", price=8.00))
    db.session.add(MenuItem(category_id=7, name="Meatball Sub", price=8.00))
    db.session.add(MenuItem(category_id=7, name="Grilled Cheese & Tomato Soup", price=5.00))
    db.session.add(MenuItem(category_id=7, name="Dino Nuggies", price=5.00))
    db.session.add(MenuItem(category_id=7, name="Chocolate Milk", price=3.00))
    
    # Add-Ons
    db.session.add(MenuItem(category_id=8, name="A Plate of Meatballs", price=5.00))
    db.session.add(MenuItem(category_id=8, name="A Whole Raw Eggplant", price=3.00))
    db.session.add(MenuItem(category_id=8, name="Breadsticks To Go", price=2.00))
    
    # Desserts
    db.session.add(MenuItem(category_id=9, name="Tiramisu ", price=8.50))
    db.session.add(MenuItem(category_id=9, name="Cannoli ", price=6.50))
    db.session.add(MenuItem(category_id=9, name="Panna Cotta", price=7.00))
    db.session.add(MenuItem(category_id=9, name="Gelato Flight", price=9.50))
    
    db.session.commit()
'''