from auth import load_users, save_users, update_profile
import os

def admin_actions():
    """Function to display admin actions."""
    try:
        while True:
            print("\nAdmin Menu")
            print("1. Manage Staff")
            print("2. View Sales Report")
            print("3. View Customer Feedback")
            print("4. Manage Users")
            print("5. Update Profile")
            print("6. Logout")
            
            choice = input("Please select an option: ")
            if choice == "1":
                manage_staff()
            elif choice == "2":
                sales_report()
            elif choice == "3":
                customer_feedback()
            elif choice == "4":
                manage_users()
            elif choice == "5":
                update_profile("admin")
            elif choice == "6":
                print("Logging out...")
                break
            else:
                print("Invalid input")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")

def manage_staff():
    """Function to manage staff members."""
    staff_list = []
    filename = "staff_data.txt"
    
    # Load existing data from file
    def load_data():
        nonlocal staff_list
        try:
            with open(filename, 'r') as file:
                staff_list = []
                for line in file:
                    if line.strip():  # Skip empty lines
                        name, role, staff_id = line.strip().split(',')
                        staff_list.append({"name": name, "role": role, "id": staff_id})
            print("Staff data loaded successfully!")
        except FileNotFoundError:
            print("No existing staff data found. Starting with empty list.")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    # Save data to file
    def save_data():
        try:
            with open(filename, 'w') as file:
                for staff in staff_list:
                    file.write(f"{staff['name']},{staff['role']},{staff['id']}\n")
            print("Staff data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    # Load data when starting
    load_data()

    try:
        while True:
                print("\nStaff Management System")
                print("1. Add Staff")
                print("2. Remove Staff")
                print("3. View All Staff")
                print("4. Update Staff Information")
                print("5. Search Staff")
                print("6. Save and Exit")
                
                choice = input("Enter your choice (1-6): ")
                
                if choice == "1":
                    print("\nAdd New Staff Member")
                    name = input("Enter staff name: ")
                    role = input("Enter role (staff/chef/manager): ").lower()
                    while role not in ['staff', 'chef', 'manager']:
                        print("Invalid role. Please enter 'staff', 'chef', or 'manager'.")
                        role = input("Enter role (staff/chef/manager): ").lower()
                        
                    staff_id = input("Enter staff ID: ")
                    # Check if ID already exists
                    if any(staff['id'] == staff_id for staff in staff_list):
                        print("Error: Staff ID already exists!")
                    else:
                        staff_list.append({"name": name, "role": role, "id": staff_id})
                        print(f"{name} added successfully!")
                        save_data()  # Save after each addition
                
                elif choice == "2":
                    print("\nRemove Staff Member")
                    staff_id = input("Enter staff ID to remove: ")
                    found = False
                    for staff in staff_list:
                        if staff["id"] == staff_id:
                            staff_list.remove(staff)
                            print(f"{staff['name']} removed successfully!")
                            save_data()  # Save after removal
                            found = True
                            break
                    if not found:
                        print("Staff not found!")
                
                elif choice == "3":
                    print("\nAll Staff Members:")
                    if not staff_list:
                        print("No staff members found.")
                    else:
                        print("{:<10} {:<20} {:<10}".format("ID", "Name", "Role"))
                        print("-" * 40)
                        for staff in sorted(staff_list, key=lambda x: x['id']):
                            print("{:<10} {:<20} {:<10}".format(staff['id'], staff['name'], staff['role']))
                
                elif choice == "4":
                    print("\nUpdate Staff Information")
                    staff_id = input("Enter staff ID to update: ")
                    for staff in staff_list:
                        if staff["id"] == staff_id:
                            print(f"Current details: {staff['name']} ({staff['role']})")
                            staff['name'] = input(f"Enter new name ({staff['name']}): ") or staff['name']
                            new_role = input(f"Enter new role ({staff['role']}): ").lower()
                            if new_role:
                                while new_role not in ['staff', 'chef', 'manager']:
                                    print("Invalid role. Please enter 'staff', 'chef', or 'manager'.")
                                    new_role = input(f"Enter new role ({staff['role']}): ").lower()
                                staff['role'] = new_role
                            print("Staff information updated successfully!")
                            save_data()  # Save after update
                            break
                    else:
                        print("Staff not found!")
                
                elif choice == "5":
                    print("\nSearch Staff")
                    search_term = input("Enter name or ID to search: ").lower()
                    found = False
                    for staff in staff_list:
                        if (search_term in staff['name'].lower()) or (search_term == staff['id'].lower()):
                            print(f"ID: {staff['id']}, Name: {staff['name']}, Role: {staff['role']}")
                            found = True
                    if not found:
                        print("No matching staff found.")
                
                elif choice == "6":
                    save_data()  # Save before exiting
                    print("Exiting staff management system.")
                    break
                
                else:
                    print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        save_data()            

def sales_report(action="generate"):
    """Function to manage sales reports."""
    REPORT_FILE = "sales_report.txt"
    
    def read_report():
        """Read and display the current sales report"""
        try:
            with open(REPORT_FILE, "r") as file:
                print("\n" + "="*50)
                print("CURRENT SALES REPORT".center(50))
                print("="*50 + "\n")
                print(file.read())
                print("="*50)
        except FileNotFoundError:
            print("No sales report found. Generating a new one...")
            generate_report()

    def generate_report():
        """Generate a new sales report with sample data"""
        # Sample sales data
        sales_data = [
            {"product": "Mo:Mo", "quantity": 5, "price": 800, "category": "Appetizer"},
            {"product": "Pizza", "quantity": 10, "price": 500, "category": "Main"},
            {"product": "Burger", "quantity": 7, "price": 300, "category": "Main"},
        ]
        
        # Calculate totals
        total_sales = sum(item["quantity"] * item["price"] for item in sales_data)
        
        # Generate report content
        report_content = [
            "RESTAURANT SALES REPORT\n",
            "="*50 + "\n",
            "{:<20} {:<10} {:<10} {:<10}\n".format("Item", "Qty", "Price", "Total"),
            "-"*50 + "\n"
        ]
        
        for item in sales_data:
            total = item["quantity"] * item["price"]
            report_content.append(
                "{:<20} {:<10} ${:<9} ${:<9}\n".format(
                    item["product"],
                    item["quantity"],
                    item["price"],
                    total
                )
            )
        
        report_content.extend([
            "="*50 + "\n",
            f"TOTAL SALES: ${total_sales}\n",
        ])
        
        # Write to file
        with open(REPORT_FILE, "w") as file:
            file.writelines(report_content)
        
        print("\nNew sales report generated successfully!")
        read_report()

    def append_sales():
        """Add new sales to the existing report"""
        try:
            # Read existing content
            with open(REPORT_FILE, "r") as file:
                existing_content = file.readlines()
            
            # Remove footer if exists
            if "Report generated" in existing_content[-1]:
                existing_content = existing_content[:-1]
            
            # Get new sales data
            new_sales = []
            while True:
                product = input("\nEnter product name (or 'done' to finish): ")
                if product.lower() == 'done':
                    break
                try:
                    quantity = int(input("Enter quantity sold: "))
                    price = float(input("Enter unit price: "))
                    category = input("Enter category: ")
                    new_sales.append({
                        "product": product,
                        "quantity": quantity,
                        "price": price,
                        "category": category
                    })
                except ValueError:
                    print("Invalid input. Please enter numbers for quantity and price.")    
            
            if not new_sales:
                print("No new sales added.")
                return
            
            # Calculate new totals
            new_total = sum(item["quantity"] * item["price"] for item in new_sales)
            
            # Find and update the total sales line
            for i, line in enumerate(existing_content):
                if line.startswith("TOTAL SALES: $"):
                    current_total = float(line.split("$")[1])
                    existing_content[i] = f"TOTAL SALES: ${current_total + new_total}\n"
                    break
            
            # Add new sales entries
            for item in new_sales:
                total = item["quantity"] * item["price"]
                existing_content.insert(-2, 
                    "{:<20} {:<10} ${:<9} ${:<9}\n".format(
                        item["product"],
                        item["quantity"],
                        item["price"],
                        total
                    )
                )
            
            # Write back to file
            with open(REPORT_FILE, "w") as file:
                file.writelines(existing_content)
            
            print(f"\nSuccessfully added {len(new_sales)} new sales entries!")
            read_report()
            
        except FileNotFoundError:
            print("No existing report found. Generate one first.")
        except ValueError:
            print("Invalid input. Please enter numbers for quantity and price.")

    # Main menu
    try:
        while True:
            print("\nRESTAURANT SALES REPORT SYSTEM")
            print("1. Generate New Report")
            print("2. View Current Report")
            print("3. Add New Sales")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1":
                generate_report()
            elif choice == "2":
                read_report()
            elif choice == "3":
                append_sales()
            elif choice == "4":
                print("Exiting sales report system.")
                break
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")

def customer_feedback():
    try:
        with open("Customer_feedback.txt", "r") as file:
            feedback_content = file.read()
            print("Customer Feedback Report:")
            print("-" * 30)
            print(feedback_content if feedback_content else "No feedback available.")
    except FileNotFoundError:
        print("No feedback file found. Please add feedback first.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

def manage_users():
    """Function to manage user credentials (admin only)"""
    try:
        while True:
            print("\nUser Management System")
            print("1. Add New User")
            print("2. View All Users")
            print("3. Remove User")
            print("4. Return to Admin Menu")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1":
                print("\nAdd New User")
                role = input("Enter role (admin/manager/chef/customer): ").lower()
                while role not in ['admin', 'manager', 'chef', 'customer']:
                    print("Invalid role. Please enter admin, manager, chef, or customer.")
                    role = input("Enter role: ").lower()
                
                name = input("Enter full name: ")
                email = input("Enter email: ")
                password = input("Enter password: ")
                
                users = load_users()
                # Check if email already exists
                if any(user['email'] == email for user in users):
                    print("Error: Email already exists!")
                else:
                    # Add to user credentials
                    users.append({"role": role, "email": email, "password": password})
                    save_users(users)
                    
                    # Add to appropriate data file based on role
                    if role in ['manager', 'chef']:
                        # Add to staff_data.txt
                        staff_id = f"{role.upper()}{len(users)}"  # Generate staff ID
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
                    
                    print(f"User {name} added successfully!")
            
            elif choice == "2":
                users = load_users()
                print("\nAll Users:")
                print("{:<10} {:<20} {:<15}".format("Role", "Email", "Password"))
                print("-" * 45)
                for user in users:
                    print("{:<10} {:<20} {:<15}".format(
                        user['role'], user['email'], '*' * len(user['password'])))
            
            elif choice == "3":
                email = input("Enter email of user to remove: ")
                users = load_users()
                user_to_remove = None
                
                # Find user to remove
                for user in users:
                    if user['email'] == email:
                        user_to_remove = user
                        break
                
                if user_to_remove:
                    # Remove from user credentials
                    users.remove(user_to_remove)
                    save_users(users)
                    
                    # Remove from appropriate data file
                    if user_to_remove['role'] in ['manager', 'chef']:
                        # Remove from staff_data.txt
                        with open("staff_data.txt", "r") as file:
                            staff = file.readlines()
                        with open("staff_data.txt", "w") as file:
                            for line in staff:
                                if email not in line:
                                    file.write(line)
                    elif user_to_remove['role'] == 'customer':
                        # Remove from customers.txt
                        with open("customers.txt", "r") as file:
                            customers = file.readlines()
                        with open("customers.txt", "w") as file:
                            for line in customers:
                                if email not in line:
                                    file.write(line)
                    
                    # Remove profile file if exists
                    profile_file = f"{user_to_remove['role']}_profile.txt"
                    try:
                        os.remove(profile_file)
                    except FileNotFoundError:
                        pass
                    
                    print(f"User {email} removed successfully!")
                else:
                    print("User not found!")
            
            elif choice == "4":
                break
            
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user") 