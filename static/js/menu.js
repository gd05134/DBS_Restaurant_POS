let orderTotal = 0;
let orderItems = {};

function loadItems(categoryId) {
    fetch(`/menu_items/${categoryId}`)
        .then(response => response.json())
        .then(items => {
            const itemsGrid = document.getElementById("itemsGrid");
            itemsGrid.innerHTML = "";
            items.forEach(item => {
                const itemButton = document.createElement("button");
                itemButton.textContent = `${item.name} - $${item.price.toFixed(2)}`;
                itemButton.onclick = () => addToOrder(item);
                itemsGrid.appendChild(itemButton);
            });
        })
        .catch(error => {
            console.error("Error loading items:", error);
        });
}

function addToOrder(item) {
    if (orderItems[item.name]) {
        currentQuantity = orderItems[item.name].quantity;
        newQuantity = currentQuantity + 1;
        orderItems[item.name] = {item: item, item_name: item.name, item_id:item.item_id, quantity: newQuantity};
    } else {
        orderItems[item.name] = {item: item, item_name: item.name, item_id:item.item_id, quantity: 1};
    }

    updateOrderList();
}


function updateOrderList() {
    const orderList = document.getElementById("orderList");
    orderList.innerHTML = "";

    orderTotal = 0;

    for (let itemName in orderItems) {
        const orderItem = orderItems[itemName];
        const orderItemElement = document.createElement("li");
        orderItemElement.classList.add("order-item");

        const itemText = document.createElement("span");
        itemText.textContent = `${orderItem.item.name} - $${orderItem.item.price.toFixed(2)} (x${orderItem.quantity})`;
        orderItemElement.appendChild(itemText);

        const removeOneButton = document.createElement("button");
        removeOneButton.textContent = "X";
        removeOneButton.classList.add("remove-one-btn");
        removeOneButton.onclick = () => {
            removeOne(itemName);
        };

        const removeAllButton = document.createElement("button");
        removeAllButton.textContent = "X All";
        removeAllButton.classList.add("remove-all-btn");
        removeAllButton.onclick = () => {
            removeAll(itemName);
        };

        orderItemElement.appendChild(removeOneButton);
        orderItemElement.appendChild(removeAllButton);

        orderList.appendChild(orderItemElement);
        orderTotal += orderItem.item.price * orderItem.quantity;
    }

    document.getElementById("orderTotal").textContent = orderTotal.toFixed(2);
}


function removeOne(itemName) {
    if (orderItems[itemName].quantity > 1) {
        orderItems[itemName].quantity -= 1;
    } else {
        delete orderItems[itemName];
    }
    updateOrderList();
}

function removeAll(itemName) {
    delete orderItems[itemName];
    updateOrderList();
}


function submitOrder() {
    const orderData = {
        table_id: tableId,
        order_items: Object.keys(orderItems).map(name => ({
            item_name: orderItems[name].item_name,
            item_id: orderItems[name].item_id,
            quantity: orderItems[name].quantity
        })),
        total_cost: orderTotal
    };

    fetch('/submit_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Order Submitted Successfully!");
            window.location.href = "/"; 
        } else {
            alert("There was an issue submitting the order.");
        }
    })
    .catch(error => {
        console.error("Error submitting order:", error);
    });
}
