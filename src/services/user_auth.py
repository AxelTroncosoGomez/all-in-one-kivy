import json
import uuid

class User:

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password
        self.is_email_verified: bool


class AuthService():
    
    def __init__(self, user: User):
        self.user = user
        self.initialize()

    def initialize(self):
        with open('users_secret.json', 'r') as file:
            self.__db = json.load(file)

    def get_id_from_user(self, username, email):
        for user in self.__db:
            if (user["username"] == username) and (user["email"] == email):
                return user["user_id"]
        return None

    def login(self, username, email, password):
        user_id = self.get_id_from_user()


    def create_user_with_email_and_password(self):
        # Generate a unique user ID
        new_user_id = str(uuid.uuid4())

        # Create user data
        new_user_data = {
            "user_id": new_user_id,
            "username": self.user.username,
            "email": self.user.email,
            "password": self.user.password,  # In a real app, hash the password before storing
            "is_email_verified": False
        }

        self.__db.append(new_user_data)

        # Save the updated list back to the JSON file
        with open('users_secret.json', 'w') as file:
            json.dump(self.__db, file, indent = 4)

        return new_user_id
    
if __name__ == "__main__":
    user = User(
        username = "axel",
        password = "axel",
        email = "axel@mail.com"
    )
    auth_user = AuthService(user)
    auth_user.create_user_with_email_and_password()

