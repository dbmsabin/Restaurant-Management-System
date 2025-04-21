from auth import update_profile

def chef_actions():
    """functions to display chef actions"""
    try:
        while True:
            print("\nChef Menu:")
            print("1. View Orders")
            print("2. Update Orders") 
            print("3. Request Ingredients")
            print("4. Update profile")
            print("5. Logout")

            choice = int(input("Please select an option: (1-5)"))
            if choice == 1:
                view_order()
            elif choice == 2:
                update_order()
            elif choice == 3:
                request_ingredients()
            elif choice == 4:
                update_profile("chef")
            elif choice == 5:
                print("Logging out...")
                break
            else:
                print("Invalid Input")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def view_order():
    """Function to view customer orders"""
    try:
        with open("orders.txt", "r") as file:
            orders = file.readlines()
            if orders:
                print("\nCurrent Orders:")
                print("{:<20} {:<15}".format("Order", "Status"))
                print("-" * 35)
                for order in orders:
                    parts = order.strip().split(',')
                    if len(parts) >= 2:
                        print("{:<20} {:<15}".format(parts[0], parts[1]))
                    else:
                        print("{:<20} {:<15}".format(parts[0], "Pending"))
            else:
                print("No orders found.")
    except FileNotFoundError:
        print("No orders file found!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def update_order():
    try:
        with open("orders.txt", "r") as file:
            orders = [line.strip().split(",") for line in file]
        if not orders:
            print("No orders to update!")
            return
        print("\nCurrent Orders:")
        for i, order in enumerate(orders, 1):
            if len(order) >= 2:
                print(f"{i}. {order[0]} - {order[1]}")
            else:
                print(f"{i}. {order[0]} - Pending")
        try:
            choice = int(input("Enter order number to update: ")) - 1
            if 0 <= choice < len(orders):
                new_status = input("Enter new status (Pending/In progress/Completed): ").capitalize()
                while new_status not in ["Pending", "In progress", "Completed"]:
                    print("Invalid status. Please enter Pending, In Progress, or Completed.")
                    new_status = input("Enter new status: ").capitalize()
                
                if len(orders[choice]) >= 2:
                    orders[choice][1] = new_status
                else:
                    orders[choice].append(new_status)
                
                with open("orders.txt", "w") as file:
                    for order in orders:
                        file.write(','.join(order) + "\n")
                print("Order updated successfully!")
            else:
                print("Invalid order number!")
        except ValueError:
            print("Please enter a valid number.")
    except FileNotFoundError:
        print("No orders file found!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def request_ingredients():
    try:
        ingredients = [
            {"category": "Vegetables", "name": "Tomatoes", "quantity": 20, "unit": "kg", "min_stock": 5},
            {"category": "Vegetables", "name": "Onions", "quantity": 15, "unit": "kg", "min_stock": 3},
            {"category": "Meat", "name": "Chicken", "quantity": 10, "unit": "kg", "min_stock": 4},
            {"category": "Dairy", "name": "Cheese", "quantity": 5, "unit": "kg", "min_stock": 2},
            {"category": "Spices", "name": "Salt", "quantity": 2, "unit": "kg", "min_stock": 1},
        ]
        with open("ingredients.txt", "w") as file:
            file.write("Category|Ingredient|Quantity|Unit|Min_Stock\n")
            for item in ingredients:
                file.write(f"{item['category']}|{item['name']}|{item['quantity']}|{item['unit']}|{item['min_stock']}\n")
                
        print("Ingredients list updated successfully!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.") 