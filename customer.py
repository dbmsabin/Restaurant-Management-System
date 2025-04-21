from auth import update_profile

def customer_actions():
    """fuctions to display customer actions"""
    try:
        while True:
            print("\nCustomer Menu: ")
            print("1. View menu and Place Order")
            print("2. View order status")
            print("3. Send feedback")
            print("4. Update Profile")
            print("5. Logout")

            choice = int(input("Please select an option (1-5): "))
            if choice == 1:
                add_order()
            elif choice == 2:
                view_order_status()
            elif choice == 3:
                send_feedback() 
            elif choice == 4:
                update_profile("customer")
            elif choice == 5:
                print("Logging out...")
                break
            else:
                print("Invalid Input")  
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def add_order():
    try:
        try:
            with open("menu.txt", "r") as file:
                menu_items = file.readlines()
                if menu_items:
                    print("\nMenu:")
                    print("{:<20} {:<10}".format("Item", "Price"))
                    print("-" * 30)
                    for item in menu_items:
                        parts = item.strip().split(',')
                        if len(parts) >= 2:
                            print("{:<20} {:<10}".format(parts[0], parts[1]))
                else:
                    print("Menu is currently empty. Please check back later.")
                    return
        except FileNotFoundError:
            print("Menu is currently empty. Please check back later.")
            return
        
        order_name = input("\nEnter order name (or 'cancel' to exit): ")
        if order_name.lower() == 'cancel':
            print("Order cancelled.")
            return

        with open("orders.txt", "a") as file:
            file.write(f"{order_name},Pending\n")
        
        print(f"Order '{order_name}' placed successfully!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def view_order_status():
    """Function to view order status."""
    try:
        with open("orders.txt", "r") as file:
            orders = file.readlines()
            if orders:
                print("\nYour Orders:")
                print("{:<20} {:<15}".format("Order", "Status"))
                print("-" * 35)
                for order in orders:
                    parts = order.strip().split(',')
                    if len(parts) >= 2:
                        print("{:<20} {:<15}".format(parts[0], parts[1]))
                    else:
                        print("{:<20} {:<15}".format(parts[0], "Pending"))
            else:
                print("You have no orders.")
    except FileNotFoundError:
        print("You have no orders.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def send_feedback():
    """Function to send feedback to admin."""
    try:
        feedback = input("Please provide your feedback (or 'cancel' to exit): ")
        if feedback.lower() == 'cancel':
            print("Feedback cancelled.")
            return
            
        with open("Customer_feedback.txt", "a") as file:
            file.write(f"{feedback}\n")

        print("Thank you for your feedback!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.") 