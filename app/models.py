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
                """SELECT id FROM users WHERE username = '{U}';""".format(
                        U=username))
        id = cursor.fetchall()
        try:
            id = id[0][0]
        except Exception:
            id = None
        cursor.close()
        return str(id)

    @staticmethod
    def get_hash_by_id(id):
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT password FROM users WHERE id = {U};""".format(
                        U=id))
        password_shash = cursor.fetchall()
        try:
            password_shash = password_shash[0][0]
        except Exception:
            password_shash = None
        cursor.close()
        return str(password_shash)

    @staticmethod
    def get_user_role_by_id(id):
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT role FROM users WHERE id = {U};""".format(
                        U=id))
        role = cursor.fetchall()
        try:
            role = role[0][0]
        except Exception:
            role = None
        cursor.close()

        if role is None:
            role = 'admin'
        elif role:
            role = 'human'
        else: 
            role = 'alien'

        return role

    @staticmethod
    def add_user(username, pasword_hash, role):
        print("add user", username, pasword_hash, role)
        pass


@login.user_loader
def load_user(username):
    return User.get_user(username=username)


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = DB.get_id_by_username(username)
        self.password_hash = False
        self.role = DB.get_user_role_by_id(self.id)
        self.planet = None

    def if_exists(self):
        return self.id

    def authenticate(self, password):
        res = check_password_hash(
            self.password_hash or DB.get_hash_by_id(self.id), str(password))
        return res

    def get_id(self):
        return self.id

    @staticmethod
    def get_user(username):
        user = User(username=username)
        if not user.if_exists():
            return None
        return user
