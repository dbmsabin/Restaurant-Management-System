from auth import load_users, authenticate_user
from admin import admin_actions
from manager import manager_actions
from chef import chef_actions
from customer import customer_actions

def main():
    try:
        while True:
            print("\nRestaurant Management System")
            login_role = input("Login as (Admin/Manager/Chef/Customer) or 'exit' to quit: ").lower().strip()
            
            if login_role == 'exit':
                print("Exiting system. Goodbye!")
                break
                
            users = load_users()
            if login_role in [user["role"] for user in users]:
                if authenticate_user(login_role):
                    if login_role == "admin":
                        admin_actions()
                    elif login_role == "manager":
                        manager_actions()
                    elif login_role == "chef":
                        chef_actions()
                    elif login_role == "customer":
                        customer_actions()
            else:
                print("Invalid role. Please try again.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

if __name__ == "__main__":
    main() 