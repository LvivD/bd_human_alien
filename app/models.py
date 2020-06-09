from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from app import login

import psycopg2


class DB:
    conn = None

    @staticmethod
    def connect():
        if DB.conn is None:
            DB.conn = psycopg2.connect(dbname='db6', user='team6',
                                       password='pas6sword',
                                       host='142.93.163.88',
                                       port='6006')

    @staticmethod
    def disconnect():
        if DB.conn is not None:
            DB.conn.close()

    @staticmethod
    def get_id_by_username(username):
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT id FROM test_table WHERE username = '{U}';""".format(
                        U=username))
        id = cursor.fetchall()
        try:
            id = id[0][0]
        except Exception:
            id = None
        cursor.close()
        return str(id)

    @staticmethod
    def get_username_by_id(id):
        return id

    @staticmethod
    def get_info_by_id(id):
        pass

    @staticmethod
    def if_user_exists(username):
        return True

    @staticmethod
    def get_hash_by_id(id):
        return generate_password_hash(id)

    @staticmethod
    def get_user_info_by_id(id):
        return 'human'

    @staticmethod
    def add_user(username, password_hash, role):
        print("add user", username, password_hash, role)
        pass


@login.user_loader
def load_user(username):
    return User.get_user(username=username)


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = DB.get_id_by_username(username)
        self.password_hash = False
        self.role = None

    def if_exists(self):
        return self.id

    def upload_data(self):
        self.role = DB.get_user_info_by_id(self.id)

    def authenticate(self, password):
        res = check_password_hash(
                self.password_hash or DB.get_hash_by_id(self.id),
                str(password))
        if res:
            self.upload_data()
        return res

    def get_id(self):
        return self.id

    @staticmethod
    def get_user(username):
        user = User(username=username)
        if not user.if_exists():
            return None
        return user
