from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from app import login


class DB:
    @staticmethod
    def connect(username):
        pass

    @staticmethod
    def disconnect(username):
        pass

    @staticmethod
    def get_id_by_username(username):
        return username

    @staticmethod
    def get_username_by_id(id):
        return id

    @staticmethod
    def if_user_exists(username):
        return True
    
    @staticmethod
    def get_hash_by_id(id):
        return generate_password_hash(id)

@login.user_loader
def load_user(username):
    return User.get_user(username=username)
    

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = id
        self.id = DB.get_id_by_username(username)
        self.password_hash = False

    def if_exists(self):
        return self.id

    def authenticate(self, password):
        return check_password_hash(self.password_hash or DB.get_hash_by_id(self.id), password)

    def get_id(self):
        return self.id

    @staticmethod
    def get_user(username):
        user = User(username=username)
        if not user.if_exists():
            return None
        return user

    
