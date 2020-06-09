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
    def template_of_cursor(command):
        cursor = DB.conn.cursor()
        cursor.execute(command)
        DB.conn.commit()
        response = cursor.fetchall()
        cursor.close()
        return response

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
    def get_all_aliens():
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT username FROM users WHERE role = False;""")
        aliens_list = cursor.fetchall()
        cursor.close()
        
        for i in range(len(aliens_list)):
            try:
                aliens_list[i] = aliens_list[i][0]
            except Exception:
                aliens_list[i] = []
        print(aliens_list)
        return aliens_list

    # @staticmethod
    # def get_all_aliens_on_the_ship(human_id):
    #     print("get_all_aliens_on_the_ship id:", human_id)
    #     command = """select username form (SELECT alien_id from alien_group where alien_group_id = (select alien_group_id from starship where id = (select place_id from users where id = (SELECT user_id from human where id = {human_id}))) as id_alien join users on id_alien.id = users.idselect username form (SELECT alien_id from alien_group where alien_group_id = (select alien_group_id from starship where id = (select place_id from users where id = (SELECT user_id from human where id = {human_id}))) as id_alien join users on id_alien.id = users.id""".format(human_id=human_id)
    #     aliens_list = DB.template_of_cursor(command)
    #     if len(aliens_list) == 0:
    #         return []
    #     for i in range(len(aliens_list)):
    #         try:
    #             aliens_list[i] = aliens_list[i][0]
    #         except Exception:
    #             aliens_list[i] = []
    #     print(aliens_list)
    #     return aliens_list

    @staticmethod
    def get_all_aliens_on_the_ship(human_id):
        print("get_all_aliens_on_the_ship id:", human_id)
        command = """SELECT alien_id from alien_group where alien_group_id = (select alien_group_id from starship where id = (select place_id from users where id = (SELECT user_id from human where id = {human_id})))""".format(
            human_id=human_id)
        response_id = DB.template_of_cursor(command)
        response = {}
        for alien in response_id:
            id = alien[0]
            command = """SELECT username FROM users where id=(select user_id from alien where id={id});""".format(
                id=id)
            name = DB.template_of_cursor(command)
            name = name[0][0]
            response[name] = id
        print(response)
        return response

    @staticmethod
    def add_user(username, password_hash, role):
        if role == 'human':
            role_to_add = True
        else:
            role_to_add = False
        command = """insert into  users values ((SELECT Max(id) + 1 from users), '{username}', '{username}', '{pasword_hash}', {role}, True, False, 1)""".format(
            username=username, pasword_hash=password_hash, role=role_to_add)
        response_id = DB.template_of_cursor(command)
        print("add user responce:",response_id)
        print("add user", username, password_hash, role)
        pass

    # людина вбиває прибульця (НАЧИНКА ФУНКЦІЇ)
    @staticmethod
    def human_kill_alien(human_id, alien_id):
        command = """INSERT INTO murder (id, human_id, alien_id, DATE) VALUES ((SELECT Max(id) + 1 from murder),{human_id}, {alien_id}, CURRENT_DATE);update users set alive = false where id = (SELECT user_id from alien where id = {alien_id});DELETE from alien_group where alien_group_id = (SELECT alien_group_id FROM starship where id = (SELECT place_id FROM users where id = (SELECT user_id from alien where id = {alien_id}))) and alien_id = {alien_id};""".format(human_id=human_id, alien_id=alien_id)
        try:
            DB.template_of_cursor(command)
        except Exception as excp:
            print("human_kill_alien exeption:",excp)
            return False
        return True



@login.user_loader
def load_user(id):
    return User.get_user(id=id)


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        _id = DB.get_id_by_username(self.username)
        self.id = _id
        if _id is not None:
            self.password_hash = DB.get_hash_by_username(username)
            self.role = DB.get_role_by_id(self.id)
        else:
            self.password_hash = None
            self.role = None
             
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
