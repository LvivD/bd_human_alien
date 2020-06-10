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
        try:
            response = cursor.fetchall()
        except:
            response = None
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
    def get_if_alive_by_id(id):
        
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT alive FROM users WHERE id = {U};""".format(
                        U=id))
        alive = cursor.fetchall()
        try:
            alive = alive[0][0]
        except Exception:
            alive = None
        cursor.close()
        print("get_if_alive_by_id", id, alive, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        return alive

    @staticmethod
    def get_all_aliens():
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT username, id FROM users WHERE role = False;""")
        aliens_list = cursor.fetchall()
        cursor.close()
        alien_dict = {} 
        for i in range(len(aliens_list)):
            try:
                alien_dict[aliens_list[i][0]] = aliens_list[i][1]
            except Exception:
                pass
        print(alien_dict)
        return alien_dict

    @staticmethod
    def get_all_humans():
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT username, id FROM users WHERE role = True;""")
        humans_list = cursor.fetchall()
        cursor.close()
        human_dict = {}
        for i in range(len(humans_list)):
            try:
                human_dict[humans_list[i][0]] = humans_list[i][1]
            except Exception:
                pass
        print(human_dict)
        return human_dict

    @staticmethod
    def get_all_ships():
        cursor = DB.conn.cursor()
        cursor.execute(
                """SELECT name, id FROM starship;""")
        ships_list = cursor.fetchall()
        cursor.close()
        ships_dict = {}
        for i in range(len(ships_list)):
            try:
                ships_dict[ships_list[i][0]] = ships_list[i][3]
            except Exception:
                pass
        print(ships_dict)
        return ships_dict

    @staticmethod
    def add_user(username, password_hash, role):
        if role == 'human':
            role_to_add = True
            command = """insert into  users values ((SELECT Max(id) + 1 from users), '{username}', '{pasword_hash}', {role}, True, False, 1)""".format(
                username=username, pasword_hash=password_hash, role=role_to_add)
        else:
            role_to_add = False
            available_ships = DB.get_ships_for_crashing()
            if len(available_ships) == 0:
                available_ships = [-1]
            else:
                available_ships = [DB.template_of_cursor("""SELECT id from starship where name = '{name}';""".format(name=available_ships[0]))[0][0]]
            command = """insert into  users values ((SELECT Max(id) + 1 from users), '{username}', '{pasword_hash}', {role}, True, True, {ship_id})""".format(
                username=username, pasword_hash=password_hash, role=role_to_add, ship_id=available_ships[0])
        
        response_id = DB.template_of_cursor(command)
        print("add user responce:",response_id)
        print("add user", username, password_hash, role)

    @staticmethod
    def get_ships_for_crashing():
        ships_names = DB.template_of_cursor("""select name from starship where (Select alive from users where id = (select max(user_id) from groups where id = group_id))=true;""")
        result = []
        for name in ships_names:
            result.append(name[0])
        print('all ships:', result)
        if not result:
            return ["No ships are available or all of them are destroyed"]
        return result

    @staticmethod
    def get_info_by_user(user_id):
        starship_id = DB.template_of_cursor("""SELECT place_id FROM users WHERE id = {user_id}""".format(user_id=user_id))[0][0]
        starship_name = DB.template_of_cursor("""SELECT name from starship where id = {starship_id}""".format(starship_id=starship_id))[0][0]
        neighbors_id = DB.template_of_cursor("""SELECT user_id FROM groups WHERE id = (select group_id from starship where id = {starship_id})""".format(starship_id=starship_id))
        aliens = {}
        humans = {}
        for id in neighbors_id:
            id = str(id[0])
            if id == str(user_id):
                continue
            role = DB.template_of_cursor("""SELECT role from users where id = {id};""".format(id=id))[0][0]
            username = DB.template_of_cursor("""SELECT username from users where id = {id};""".format(id=id))[0][0]
            if role:
                humans[username] = id
            if role is False:
                aliens[username] = id 
            
        print('get_info_by_user')
        print(starship_name, humans, aliens)
        return (starship_name, starship_id), humans, aliens
        
    @staticmethod
    def get_ships_dict():
        pass

    @staticmethod
    def alien_take_human_to_ship(alien_id, human_id):
        starship_id = DB.get_info_by_user(alien_id)[0][1]
        DB.action_1(alien_id, human_id, starship_id, 'CURRENT_DATE')

    # прибулець викрадає людину на корабель
    @staticmethod
    def action_1(alien_id, human_id, starship_id, date):
        command = """INSERT INTO theft VALUES ((select max(id)+1 from theft), {alien_id}, {human_id}, {starship_id}, CURRENT_DATE); update users set in_starship = true where id = {human_id}; update users set place_id = {starship_id} where id = {human_id}; Insert into groups values((select group_id from starship where id = {starship_id}), {human_id}); Insert into human_travel_history values ((select max(id) + 1 from human_travel_history), {starship_id}, {human_id}, CURRENT_DATE, null);""".format(alien_id=alien_id, human_id=human_id, starship_id=starship_id)
        DB.template_of_cursor(command)


    # 2
    @staticmethod
    def ships_visited(human, frm, to):
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT name FROM (SELECT starship_id FROM human_travel_history WHERE human_id = {Human} AND ((from_date < '{From}' AND (to_date is null OR to_date > '{From}')) OR (from_date < '{To}' and from_date > '{From}')) GROUP BY starship_id) AS tb INNER JOIN starship ON starship.id = tb.starship_id""".format(
                Human=human, From=frm, To=to))

        line = """{Human} from {From} to {To} have been on: """.format(Human=human, From=frm, To=to)
        DB.conn.commit()
        names = cursor.fetchall()
        for i in range(len(names) - 1):
            line += names[i][0] + ', '
        cursor.close()
        if names:
            line += names[-1][0] + '. '

            return line
        else:
            return ''
    
    # 3 works
    @staticmethod
    def get_all_who_theft_me_more_then_n(human, frm, to, n):
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT username FROM (SELECT alien_id FROM theft WHERE human_id = {Human} AND date BETWEEN '{From}' AND '{To}' GROUP BY alien_id HAVING COUNT(alien_id) >= {N}) as tb INNER JOIN users ON users.id = tb.alien_id""".format(
                Human=human, From=frm, To=to, N=n))
        DB.conn.commit()
        line = 'Was stolen by: '
        DB.conn.commit()
        aliens = cursor.fetchall()
        for i in range(len(aliens) - 1):
            line += aliens[i][0] + ', '
        cursor.close()

        if len(aliens):
            line += aliens[-1][0] + '. '
            print('!!!!!!!!!!!!! in get_all_who_theft_me_more_then_n res:', line)
            return line
        return ''

    # 4 works
    @staticmethod
    def killed_by_me(human, frm, to):
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT username FROM (SELECT alien_id FROM murder WHERE human_id = {Human} AND date BETWEEN '{From}' AND '{To}') AS tb INNER JOIN users ON users.id = tb.alien_id""".format(
                Human=human, From=frm, To=to))
        DB.conn.commit()
        line = 'Have murdered: '
        aliens = cursor.fetchall()
        for i in range(len(aliens) - 1):
            line += aliens[i][0] + ', '
        cursor.close()
        if aliens:
            line += aliens[-1][0] + '. '
            print('!!!!!!!!!!!!! in killed_by_me res:', line)
            return line
        else:
            return "You haven't murdered anyone."

    # 5 - works
    @staticmethod
    def theft_and_killed_by_me(human):
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT username FROM (SELECT thefts.alien_id FROM
            (SELECT alien_id FROM theft WHERE human_id = {Human}) AS thefts INNER JOIN
            (SELECT alien_id FROM murder WHERE human_id = {Human}) AS murdered ON thefts.alien_id = murdered.alien_id) AS tb
            INNER JOIN users ON users.id = tb.alien_id""".format(Human=human))
        DB.conn.commit()
        line = 'Theft me and I took revenge on: '
        aliens = cursor.fetchall()
        for i in range(len(aliens) - 1):
            line += aliens[i][0] + ', '
        if len(aliens) > 0:
            line += aliens[-1][0] + '. '
        cursor.close()
        if aliens:
            return line
        return 'No one have theft me and I have killed him.'

    # 10 - works !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    @staticmethod
    def experimented_by_n(human, frm, to, n):
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT count(*) FROM experiment INNER JOIN (SELECT id, count(id) as cnt FROM groups GROUP BY id) AS tb ON experiment.group_id = tb.id  WHERE group_id = {Human} AND date BETWEEN '{From}' AND '{To}' AND cnt >= {N}""".format(
                Human=human, From=frm, To=to, N=n))

        DB.conn.commit()
        id = cursor.fetchall()
        cursor.close()
        return 'Have taken part in ' + str(id[0][0]) + ' experiments from ' + str(frm) + ' to ' + str(to) + '. with more then ' + str(n) + 'alien`s.'
    
    # 9 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    @staticmethod
    def excursions_by_alien_with_more_then_n(alien, frm, to, n):
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT count(*) FROM excursion INNER JOIN (SELECT id, count(id) as cnt FROM groups GROUP BY id) AS tb ON excursion.group_id = tb.id  WHERE alien_id = {Alien} AND date BETWEEN '{From}' AND '{To}' AND cnt >= {N}""".format(
                Alien=alien, From=frm, To=to, N=n))

        DB.conn.commit()
        id = cursor.fetchall()
        cursor.close()
        return 'Have lead ' + str(id[0][0]) + ' excursion with more then ' + str(n) + ' people from ' + str(frm) + ' to ' + str(to) + '. '

    # людина вбиває прибульця
    @staticmethod
    def action_6(human_id, alien_id, date):
        command = """Insert into murder values ((select max(id) + 1 from murder), {human_id}, {alien_id}, {date}); Update users set alive= false where id = {alien_id}; delete from groups where id = (select group_id from starship where id = (select place_id from users where id = {alien_id})) and user_id = {alien_id};""".format(
            alien_id=alien_id, human_id=human_id, date=date)
        DB.template_of_cursor(command)

    @staticmethod
    def human_kill_alien(human_id, alien_id):
        try:
            DB.action_6(human_id, alien_id, 'CURRENT_DATE')
            return True
        except Exception as exc:
            print("human_kill_alien", exc)
            return False

    # людина тікає з космічного корабля
    @staticmethod
    def action_2(human_id, starship_id, date):
        command = """INSERT INTO escapism values((select max(id)+1 from escapism), {human_id}, {starship_id}, {date}); update users set in_starship = false where id = {human_id}; update users set place_id = 1 where id = {human_id}; DELETE from groups where id = (select group_id from starship where id = {starship_id}) and user_id = {human_id}; Update human_travel_history set to_date = {date} where starship_id = {starship_id} and human_id={human_id} and to_date=null;""".format(
            starship_id=starship_id, human_id=human_id, date=date)
        DB.template_of_cursor(command)

    # людина тікає з космічного корабля
    @staticmethod
    def escape_from_ship(human_id):
        starship_id = DB.get_info_by_user(human_id)[0][1]
        DB.action_2(human_id, starship_id, 'CURRENT_DATE')

    # корабель розбивається
    @staticmethod
    def action_7(starship_id, date):
        command = """Insert into crash values ((select max(id)+1 from crash), {starship_id}, {date});""".format(
            starship_id=starship_id, date=date)
        DB.template_of_cursor(command)
        neighbors_id = DB.template_of_cursor(
            """SELECT user_id FROM groups WHERE id = (select group_id from starship where id = {starship_id})""".format(
                starship_id=starship_id))
        for id in neighbors_id:
            id = str(id[0])
            DB.template_of_cursor(
                """UPDATE users set alive = false where id= {id};""".format(
                    id=id))
    
    @staticmethod
    def destroy_ship(starship_name):
        DB.action_7(
            starship_id=DB.template_of_cursor("""SELECT id from starship where name = '{name}';""".format(name=starship_name))[0][0], 
            date='CURRENT_DATE')

    # 6 works
    @staticmethod
    def aliens_that_theft_more_then_n(frm, to, n):
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT username FROM (SELECT alien_id FROM
            (SELECT alien_id, human_id FROM theft WHERE date BETWEEN '{From}' AND '{To}' GROUP BY alien_id, human_id)
            as thefts GROUP BY alien_id HAVING COUNT(alien_id) >= {N}) AS tb
            INNER JOIN users ON users.id = tb.alien_id""".format(From=frm, To=to, N=n))

        DB.conn.commit()
        line = "Aliens that have stolen more then N different people during period " + str(frm) + ' - ' + str(to) + ': '
        aliens = cursor.fetchall()
        for i in range(len(aliens) - 1):
            line += aliens[i][0] + ', '
        cursor.close()
        if aliens:
            line += aliens[-1][0] + '. '

            return line
        return 'No one achieved it.'

    # 7 works
    @staticmethod
    def were_thefted_more_then_n_times(frm, to, n):
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT username FROM (SELECT human_id FROM theft WHERE date BETWEEN '{From}' AND '{To}' GROUP BY human_id HAVING COUNT(human_id) >= {N}) AS tb
            INNER JOIN users ON users.id = tb.human_id""".format(From=frm, To=to, N=n))
        DB.conn.commit()
        line = "Thefted more then " + str(n) + " times: "
        humans = cursor.fetchall()
        for i in range(len(humans) - 1):
            line += humans[i][0] + ', '
        cursor.close()
        if humans:
            line += humans[-1][0] + '. '

            return line
        return 'No human fulfill the condition.'

    # 8 works
    @staticmethod
    def common_exc_and_exp_for_human_and_alien(human, alien, frm, to):
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT id, 'excursion' as type FROM excursion WHERE alien_id = {Alien} AND date BETWEEN '{From}' AND '{To}' AND EXISTS (SELECT count(*) FROM groups WHERE id = {Human})
            UNION SELECT id, 'experiment' as type FROM experiment WHERE human_id = {Human} AND date BETWEEN '{From}' AND '{To}' AND EXISTS (SELECT count(*) FROM groups WHERE id = {Alien})""".format(
                Human=human, Alien=alien, From=frm, To=to))
        excursions = []
        experiments = []
        DB.conn.commit()
        exc_exp = cursor.fetchall()
        for i in exc_exp:
            if i[1] == 'excursion':
                excursions.append(i[0])
            else:
                experiments.append(i[0])
        line = 'Excursions: '
        for i in range(len(excursions) - 1):
            line += str(excursions[i]) + ', '
        if len(excursions):
            line += str(excursions[-1]) + '.'
        line += '\nExperiments: '
        for i in range(len(experiments) - 1):
            line += str(experiments[i]) + ', '
        if len(experiments):
            line += str(experiments[-1]) + '.'
        cursor.close()
        if exc_exp:
            return line
        return 'No excursion'

    # 11 - works
    @staticmethod
    def thefts_by_month():
        cursor = DB.conn.cursor()
        cursor.execute(
            """SELECT date_trunc( 'month', date ), count(*)  from theft group by date_trunc( 'month', date )""")
        DB.conn.commit()
        line = []
        thefts_by_month = cursor.fetchall()
        for i in thefts_by_month:
            line.append('In ' + str(i[0]) + ' were ' + str(i[1]) + ' thefts.')
        cursor.close()
        if thefts_by_month:
            return line
        else:
            return ['The are no stealts at all']





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
            # self.alive = DB.get_if_alive_by_id(self.id)
        else:
            self.password_hash = None
            self.role = None
            # self.alive = False

    def if_exists(self):
        return self.password_hash

    def authenticate(self, password):
        res = check_password_hash(self.password_hash, str(password)) # and self.alive
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
