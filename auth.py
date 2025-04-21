def load_users():
    """Load users from file"""
    try:
        with open("user_credentials.txt", 'r') as file:
            users = []
            for line in file:
                if line.strip():
                    role, email, password = line.strip().split(',')
                    users.append({"role": role, "email": email, "password": password})
            return users
    except FileNotFoundError:
        # Create default users if file doesn't exist
        default_users = [
            {"role": "admin", "email": "admin", "password": "admin123"},
            {"role": "manager", "email": "manager", "password": "manager123"},
            {"role": "chef", "email": "chef", "password": "chef123"},
            {"role": "customer", "email": "customer", "password": "customer123"}
        ]
        save_users(default_users)
        return default_users

def save_users(users):
    """Save users to file"""
    with open("user_credentials.txt", 'w') as file:
        for user in users:
            file.write(f"{user['role']},{user['email']},{user['password']}\n")

def authenticate_user(role, max_attempts=3):
    """Function to authenticate a user based on role."""
    users = load_users()
    try:
        role_users = [user for user in users if user["role"] == role]
        if not role_users:
            print(f"No users found with role {role}")
            return False
            
        attempt = 0
        while attempt < max_attempts:
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            
            for user in role_users:
                if email == user["email"] and password == user["password"]:
                    print(f"You have successfully logged in as {role}")
                    return True
            
            attempt += 1
            print("Incorrect email or password. Please try again.")
            if attempt == max_attempts:
                print("Too many attempts! Try again later.")
                return False
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return False

def update_profile(role):
    """Function to update user profile and credentials"""
    profile_file = f"{role}_profile.txt"
    users = load_users()
    
    try:
        # Get current user's email
        current_email = None
        for user in users:
            if user["role"] == role:
                current_email = user["email"]
                break
        
        if not current_email:
            print("Error: Couldn't find your user account!")
            return
            
        current_name = ""
        current_phone = ""
        
        try:
            with open(profile_file, "r") as file:
                profile_data = file.readlines()
                if len(profile_data) >= 2:
                    current_name = profile_data[0].split(":")[1].strip()
                    current_phone = profile_data[1].split(":")[1].strip()
        except FileNotFoundError:
            print("No profile found. Creating a new profile.")
        
        print("\nCurrent Profile Information:")
        print(f"Name: {current_name if current_name else 'Not set'}")
        print(f"Email: {current_email}")
        print(f"Phone: {current_phone if current_phone else 'Not set'}")

        print("\nEnter new profile details (leave blank to keep current):")
        name = input(f"Name ({current_name}): ") or current_name
        new_email = input(f"New Email ({current_email}): ") or current_email
        new_password = input("New Password (leave blank to keep current): ")
        phone = input(f"Phone ({current_phone}): ") or current_phone

        # Update user credentials if email or password changed
        if new_email != current_email or new_password:
            for user in users:
                if user["email"] == current_email and user["role"] == role:
                    if new_email != current_email:
                        # Check if new email already exists
                        if any(u['email'] == new_email for u in users if u != user):
                            print("Error: Email already in use by another account!")
                            return
                        user["email"] = new_email
                    if new_password:
                        user["password"] = new_password
                    save_users(users)
                    print("Login credentials updated successfully!")
                    break

        # Save profile information
        with open(profile_file, "w") as file:
            file.write(f"Name: {name}\n")
            file.write(f"Phone: {phone}\n")

        print("Profile updated successfully!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.") 