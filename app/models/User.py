from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def register(self,info):
        password = info['password']
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not info['first_name']:
            errors.append('name cannot be blank')
        elif len(info['first_name']) < 2:
            errors.append('name must be at least 2 characters long')
        if not info['last_name']:
            errors.append('Last Name cannot be blank')
        elif len(info['last_name']) < 2:
            errors.append('Last Name must be at least 2 characters long')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['pw_confirmation']:
            errors.append('Password and confirmation must match!')

        if errors:
            return {"status": False, "errors": errors}
        else:
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (first_name, last_name, email, pw_hash, DOB) VALUES (:first_name, :last_name, :email, :password, :dob);"
            data = {
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'email': info['email'],
                'password': hashed_pw,
                'dob': info['dob']
            }
            self.db.query_db(query, data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return { "status": True, "user": users[0] }

    def login_user(self, info):

        password = info['password']

        user_query = "SELECT * FROM users WHERE email = :email"
        user_data = {'email': info['email']}

        user = self.db.query_db(user_query, user_data)


        if user:
            name = user[0]['first_name']
            id = user[0]['id']
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
                return {'name':name, 'id':id}
        return False

    def get_user_id(self,id):
        get_id_query = "SELECT * FROM users WHERE id= :id"
        data = {
            'id':id
        }
        return self.db.query_db(get_id_query, data)

    def show_friends(self,id):
        join = "SELECT * FROM users LEFT JOIN friendships ON users.id = friendships.user_id LEFT JOIN users AS users2 on users2.id = friendships.friend_id WHERE users.id = :id AND users.id != :id"
        data = {'id':id}
        return self.db.query_db(join,data)

    def get_other_users(self,id):
        get_all = "SELECT * FROM users AS users2 WHERE users2.id NOT IN (SELECT user_id FROM friendships WHERE id=:id) AND users2.id != :id"
        data = {'id':id}
        return self.db.query_db(get_all, data)

    def add_event2(self,edata):
        query = 'INSERT into events (name, date, location, description, max, host_id) values(:name, :date, :location, :description, :max, :host_id)'
        data = {
            "name" : edata['name'],
            "date" : edata['date'],
            "location" : edata['location'],
            'description': edata['description'],
            'max': edata['max'],
            'host_id': edata['host_id']
        }
        self.db.query_db(query, data)
        return True

    def get_events_hosting(self,id):
        query = 'SELECT * FROM events WHERE host_id = :id'
        data = {
            'id': id
        }
        return self.db.query_db(query, data)

    def get_events_attending(self,id):

        return self.db.query_db(query, data)

    def get_event(self,id):
        query = 'SELECT * FROM events WHERE id = :id'
        data = {
            'id': id
        }
        return self.db.query_db(query, data)
