from auth import load_users, save_users, update_profile

def manager_actions():
    """functions to display manager actions."""
    try:
        while True:
            print("\nManager Menu")  
            print("1. Manage Customer")  
            print("2. Manage menu categories and pricing")
            print("3. View ingredients list requested by chef")
            print("4. Create New Account")
            print("5. Update own profile")
            print("6. Logout")

            choice = int(input("Please select an option (1-6): "))
            if choice == 1:
                manage_customer()
            elif choice == 2:
                manage_menu()
            elif choice == 3:
                view_ingredients()
            elif choice == 4:
                create_new_account()
            elif choice == 5:
                update_profile("manager")   
            elif choice == 6:
                print("Logging out...")
                break
            else:
                print("Invalid input")
    except KeyboardInterrupt:
            print("\nOperation cancelled by user.")

def manage_customer():
    customer_file = "customers.txt"  
    try:
        while True:
            print("\nCustomer Management Menu:")
            print("1. View Customers")
            print("2. Add Customer")
            print("3. Update Customer")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == "1":  
                # View customer details
                try:
                    with open(customer_file, "r") as file:
                        customers = file.readlines()
                        if customers:
                            print("\nCustomer List:")
                            print("{:<30} {:<30}".format("Name", "Email"))
                            print("-" * 60)
                            for customer in customers:
                                parts = customer.strip().split(", ")
                                if len(parts) >= 2:
                                    name = parts[0].split(": ")[1]
                                    email = parts[1].split(": ")[1]
                                    print("{:<30} {:<30}".format(name, email))
                        else:
                            print("No customers found.")
                except FileNotFoundError:
                    print("No customer file found. Please add customers first.")

            elif choice == "2":  
                # Add a new customer
                name = input("Enter customer name: ")
                email = input("Enter customer email: ")
                password = input("Enter customer password: ")

                # Check if email already exists in user credentials
                users = load_users()
                if any(user['email'] == email for user in users):
                    print("Error: Email already exists!")
                    continue

                # Add to customer list
                with open(customer_file, "a") as file:
                    file.write(f"Name: {name}, Email: {email}\n")

                # Add to user credentials
                users.append({"role": "customer", "email": email, "password": password})
                save_users(users)

                print("Customer added successfully!")

            elif choice == "3":  
                # Update existing customer details
                try:
                    with open(customer_file, "r") as file:
                        customers = file.readlines()

                    if not customers:
                        print("No customers to update.")
                        continue

                    print("\nExisting Customers:")
                    for i, customer in enumerate(customers, start=1):
                        parts = customer.strip().split(", ")
                        if len(parts) >= 2:
                            name = parts[0].split(": ")[1]
                            email = parts[1].split(": ")[1]
                            print(f"{i}. {name} ({email})")
                    
                    try:
                        index = int(input("Enter the customer number to update: ")) - 1
                        if 0 <= index < len(customers):
                            name = input("Enter new name: ")
                            new_email = input("Enter new email: ")
                            new_password = input("Enter new password (leave blank to keep current): ")

                            # Update customer list
                            customers[index] = f"Name: {name}, Email: {new_email}\n"

                            # Update user credentials
                            users = load_users()
                            for user in users:
                                if user["role"] == "customer" and user["email"] == email:
                                    user["email"] = new_email
                                    if new_password:
                                        user["password"] = new_password
                                    break
                            save_users(users)

                            with open(customer_file, "w") as file:
                                file.writelines(customers)

                            print("Customer updated successfully!")
                        else:
                            print("Invalid customer number.")
                    except ValueError:
                        print("Please enter a valid number.")

                except FileNotFoundError:
                    print("No customer file found. Please add customers first.")

            elif choice == "4":  
                # Exit the program
                print("Exiting Customer Management...")
                break

            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def manage_menu():
    try:
        while True:
            print("\nMenu Management:")
            print("1. View Menu")
            print("2. Add Item")
            print("3. Remove Item")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ")
            if choice == "1":
                try:
                    with open("menu.txt", "r") as file:
                        menu_items = file.readlines()
                        if menu_items:
                            print("\nCurrent Menu:")
                            print("{:<20} {:<10}".format("Item", "Price"))
                            print("-" * 30)
                            for item in menu_items:
                                parts = item.strip().split(',')
                                if len(parts) >= 2:
                                    print("{:<20} {:<10}".format(parts[0], parts[1]))
                        else:
                            print("Menu is empty")
                except FileNotFoundError:
                    print("Menu is empty")

            elif choice == "2":
                try:
                    item = input("Enter item name: ")
                    price = input("Enter item price: ")
                    with open("menu.txt", "a") as file:
                        file.write(f"{item},{price}\n")
                    print("Item added successfully!")
                except Exception as e:
                    print(f"Error adding item: {e}")

            elif choice == "3":
                item = input("Enter item name to remove: ")
                try:
                    with open("menu.txt", "r") as file:
                        lines = file.readlines()
                    with open("menu.txt", "w") as file:
                        found = False
                        for line in lines:
                            if not line.startswith(item + ","):
                                file.write(line)
                            else:
                                found = True
                        if not found:
                            print("Item not found!")
                        else:
                            print("Item removed successfully!")
                except FileNotFoundError:
                    print("Menu is empty")

            elif choice == "4":
                break
            else:
                print("Invalid choice!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def view_ingredients():
    """Function to view ingredients list"""
    try:
        with open("ingredients.txt", "r") as file:
            ingredients = file.readlines()
            if ingredients:
                print("\nIngredients List:")
                print("{:<15} {:<15} {:<10} {:<10} {:<10}".format(
                    "Category", "Ingredient", "Quantity", "Unit", "Min Stock"))
                print("-" * 60)
                for line in ingredients[1:]:  # Skip header
                    parts = line.strip().split('|')
                    if len(parts) >= 5:
                        print("{:<15} {:<15} {:<10} {:<10} {:<10}".format(
                            parts[0], parts[1], parts[2], parts[3], parts[4]))
            else:
                print("No ingredients found.")
    except FileNotFoundError:
        print("No ingredients file found. Chef needs to request ingredients first.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def create_new_account():
    """Function for manager to create new chef or customer accounts"""
    try:
        print("\nCreate New Account")
        print("1. Create Chef Account")
        print("2. Create Customer Account")
        print("3. Back to Manager Menu")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "3":
            return
            
        if choice not in ["1", "2"]:
            print("Invalid choice!")
            return
            
        role = "chef" if choice == "1" else "customer"
        name = input(f"Enter full name for new {role}: ")
        email = input(f"Enter email for new {role}: ")
        password = input(f"Enter password for new {role}: ")
        
        users = load_users()
        
        # Check if email already exists
        if any(user['email'] == email for user in users):
            print("Error: Email already exists!")
            return
            
        # Add to user credentials
        users.append({"role": role, "email": email, "password": password})
        save_users(users)
        
        # Add to appropriate data file based on role
        if role == 'chef':
            # Add to staff_data.txt
            staff_id = f"CH{len(users)}"  # Generate chef ID
            with open("staff_data.txt", "a") as file:
                file.write(f"{name},{role},{staff_id}\n")
        elif role == 'customer':
            # Add to customers.txt
            with open("customers.txt", "a") as file:
                file.write(f"Name: {name}, Email: {email}\n")
        
        # Create profile file
        profile_file = f"{role}_profile.txt"
        with open(profile_file, "w") as file:
            file.write(f"Name: {name}\n")
            file.write(f"Phone: \n")  # Phone can be updated later
        
        print(f"New {role} account created successfully!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.") 