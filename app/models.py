from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from app import login


class db:
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
    active_user = User(username=username)
    return active_user
    

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = id
        self.is_authenticated = False
        self.id = db.get_id_by_username(username)
        self.password_hash = False

    def if_exists(self):
        return self.id

    def authenticate(self, password):
        if check_password_hash(self.password_hash or db.get_hash_by_id(self.id), password):
            self.is_authenticated = True
        else:
            self.is_authenticated = False
        return self.is_authenticated

    def is_authenticated(self):
        return self.is_authenticated

    
