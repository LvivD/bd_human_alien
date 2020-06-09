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
        print("get_id_by_username", username)
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT id FROM users WHERE username = '{U}';""".format(
                        U=username))
        id = cursor.fetchall()
        DB.conn.commit()
        try:
            id = id[0][0]
        except Exception:
            id = None
        cursor.close()
        if id:
            return str(id)
        return id

    @staticmethod
    def get_username_by_id(id):
        print("get_username_by_id", id)
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT username FROM users WHERE id = {U};""".format(
                        U=id))
        username = cursor.fetchall()
        DB.conn.commit()
        try:
            username = username[0][0]
        except Exception:
            username = False
        cursor.close()
        if username:
            return str(username)
        return username

    @staticmethod
    def get_hash_by_username(username):
        print("get_hash_by_username", username)
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT password FROM users WHERE username = '{U}';""".format(
                        U=username))
        password_hash = cursor.fetchall()
        DB.conn.commit()
        try:
            password_hash = password_hash[0][0]
        except Exception:
            password_hash = False
        cursor.close()
        if password_hash:
            return str(password_hash)
        return password_hash

    @staticmethod
    def get_hash_by_id(id):
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT password FROM users WHERE id = {U};""".format(
                        U=id))
        password_shash = cursor.fetchall()
        DB.conn.commit()
        try:
            password_shash = password_shash[0][0]
        except Exception:
            password_shash = False
        cursor.close()
        return str(password_shash)

    @staticmethod
    def get_role_by_id(id):
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
        elif role is True:
            role = 'human'
        elif role is False: 
            role = 'alien'
        else:
            role = None

        return role
    
    @staticmethod
    def get_planet_by_id(id):
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT planet FROM users WHERE id = {U};""".format(
                        U=id))
        planet = cursor.fetchall()
        try:
            planet = planet[0][0]
        except Exception:
            planet = None
        cursor.close()
        return planet

    @staticmethod
    def add_user(username, password_hash, role):
        print("add user", username, password_hash, role)
        pass


@login.user_loader
def load_user(id):
    return User.get_user(id=id)


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        _id = DB.get_id_by_username(self.username)
        self.id = _id
        self.password_hash = DB.get_hash_by_username(username)
        self.role = DB.get_role_by_id(self.id)
        self.planet = DB.get_planet_by_id(self.id)

    def if_exists(self):
        return self.password_hash

    def authenticate(self, password):
        res = check_password_hash(self.password_hash, str(password))
        return res

    def get_id(self):
        return self.id

    @staticmethod
    def get_user(id):
        username = DB.get_username_by_id(id)
        user = User(username=username)
        if not user.if_exists():
            return None
        return user
