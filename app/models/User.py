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
            query = "INSERT INTO users (first_name, last_name, email, pw_hash, DOB, likes, dislikes) VALUES (:first_name, :last_name, :email, :password, :dob, 0, 0);"
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

    def create_dog(self,info,id):
        id=id
        query2 = 'INSERT INTO dogs (name, type, user_id) values (:name, :type, :user_id)'
        data2 = {
            'name' : info['name'],
            'type':info['type'],
            'user_id' : id
        }
        self.db.query_db(query2, data2)
        return True

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
            else:
                return False


    def add_message_model(self, message_info):
        query = "INSERT INTO events (name, date, location, description, host_id) VALUES (:name, :date, :location, :description, :host_id)"
        data = {
            'name': message_info['headline'],
            'date': message_info['date'],
            'location':message_info['location'],
            'description': message_info['message'],
            'host_id': message_info['host_id']

        }

        return self.db.query_db(query, data)

    def append_message_model(self):
        query = "SELECT users.first_name, users.last_name, events.id as id, events.name as Headline, events.description as Description FROM users JOIN events on users.id = events.host_id ORDER BY id desc"
        append_message = self.db.query_db(query)
        return append_message



    def get_user_id(self,id):
        get_id_query = "SELECT * FROM users WHERE id= :id"
        data = {
            'id':id
        }
        return self.db.query_db(get_id_query, data)

    def show_friends(self,id):
        join = "SELECT * FROM users JOIN friendships ON users.id = friendships.user_id LEFT JOIN users AS users2 on users2.id = friendships.friend_id WHERE users.id = :id"
        data = {'id':id}
        return self.db.query_db(join,data)

    def get_other_users(self,id):
        get_all = "SELECT * FROM users WHERE users.id NOT IN (SELECT friend_id FROM friendships WHERE user_id = :id) AND users.id != :id"
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
        query = 'SELECT * FROM users_attending LEFT JOIN events ON users_attending.event_id = events.id WHERE user_id = :id'
        data = {
            'id': id
        }
        return self.db.query_db(query, data)

    def get_event(self,id):
        query = 'SELECT * FROM events WHERE id = :id'
        data = {
            'id': id
        }
        return self.db.query_db(query, data)


    def attend(self,adata):
        query = 'INSERT into users_attending (user_id, event_id) values(:user_id, :event_id)'
        data = {
            "user_id": adata['user_id'],
            "event_id": adata['event_id']
        }

        response = self.db.query_db(query, data)
        return True

    def get_attending_people(self,id):
        query = "SELECT user_id, event_id, first_name, last_name, email FROM users_attending LEFT JOIN users on users_attending.user_id = users.id WHERE event_id = :id"
        data = {
            'id': id
        }
        return self.db.query_db(query, data)

    def stop_attend(self,adata):
        query = 'DELETE FROM users_attending WHERE user_id = :user_id AND event_id = :event_id'
        data = {
            'user_id' : adata['user_id'],
            'event_id' : adata['event_id']
        }
        response = self.db.query_db(query, data)
        return True

    def add_friend_now(self,info):
        query = "INSERT INTO friendships (user_id, friend_id) VALUES (:user_id, :friend_id)"
        data = {
            'user_id': info['user_id'],
            'friend_id': info['friend_id']
        }
        return self.db.query_db(query,data)

    def remove_friend_now(self,info):
        query = "DELETE FROM friendships WHERE user_id = :user_id AND friend_id = :friend_id"
        data = {
            'user_id': info['user_id'],
            'friend_id':info['friend_id']
        }
        return self.db.query_db(query, data)

    def like(self, info):
        data = {
            'url_id': info['url_id'],
            'id': info['id'],
            'like':info['like']
        }
        user_query ="INSERT INTO likes (liker, liked) VALUES (:id, :url_id)"
        insert_like = self.db.query_db(user_query, data)

        if info['like'] == 'yes':
            add_query = "UPDATE users SET likes = likes+1 WHERE id = :url_id"
            update_count = self.db.query_db(add_query, data)
        elif info['like'] == 'no':
            add_query = "UPDATE users SET dislikes = dislikes+1 WHERE id = :url_id"
            update_count = self.db.query_db(add_query, data)
        return True

    def get_likes(self, url_id):
        get_count = 'SELECT likes, dislikes FROM users WHERE id = :url_id'
        data = {'url_id':url_id}
        gets_counts = self.db.query_db(get_count,data)
        
        summ = gets_counts[0]['likes'] + gets_counts[0]['dislikes']
        if summ!=0:
            result = (float(gets_counts[0]['likes'])/summ)*100
        else:
            result = 100
        return int(result)

    def update_user(self, info):
        update_query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, DOB = :DOB, description = :description WHERE id = :id"
        data = {
            'first_name': info['first_name'],
            'last_name': info['last_name'],
            'email': info['email'],
            'DOB': info['DOB'],
            'description': info['description'],
            'id': info['id']
        }
        return self.db.query_db(update_query, data)

    def post_message(self,id,mdata):
        id=id
        query = "INSERT into messages (message, created_at, updated_at, user_id, rec_id) values(:message, NOW(), NOW(), :user_id, :rec_id)"
        data = {
            'message': mdata['message'],
            'user_id': mdata['user_id'],
            'rec_id': id,
        }
        self.db.query_db(query, data)
        return True

    def post_comment(self,cdata):
        query = "INSERT into comments (comment, created_at, updated_at, message_id, user_id) values(:comment, NOW(), NOW(), :msg_id, :user_id)"
        data = {
            'comment': cdata['comment'],
            'msg_id': cdata['message_id'],
            'user_id': cdata['uid']
        }
        self.db.query_db(query, data)
        return True

    def get_messages(self,id):
        query = "SELECT first_name,last_name,messages.created_at,messages.id AS message_id,message FROM messages LEFT JOIN users ON users.id = messages.user_id WHERE rec_id = :rec_id ORDER BY messages.id DESC"
        data = {
            'rec_id':id
        }
        return self.db.query_db(query, data)

    def get_comments(self,id):
        query = "SELECT users.id, first_name, last_name, comment, comments.created_at, comments.message_id FROM users JOIN comments ON users.id = comments.user_id ORDER BY comments.created_at"
        return self.db.query_db(query)


    def edit_dog(self,ddata):
        query = 'UPDATE dogs SET name=:name, type=:type, description=:description, DOB=:DOB, gender=:gender WHERE user_id = :user_id'
        data = {
            'name' : ddata['name'],
            'type' : ddata['type'],
            'description': ddata['description'],
            'DOB': ddata['DOB'],
            'gender': ddata['gender'],
            'user_id': ddata['user_id']
        }
        self.db.query_db(query, data)
        return True

    def get_dog(self,id):
        query = 'SELECT * FROM dogs WHERE user_id = :id'
        data = {
            'id': id
        }
        return self.db.query_db(query, data)

    def edit_user(self,udata):
        query = 'UPDATE users SET first_name=:first_name, last_name=:last_name, email=:email, DOB=:DOB, description=:description WHERE id = :id'
        data = {
            'id':udata['id'],
            'first_name': udata['first_name'],
            'last_name': udata['last_name'],
            'email': udata['email'],
            'DOB': udata['DOB'],
            'description': udata['description'],
        }
        return self.db.query_db(query, data)
