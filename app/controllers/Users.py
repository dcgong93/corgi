from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db

    def index(self):

        return self.load_view('index.html')

    def dashboard_control(self):
        print session['id']
        return self.load_view('dashboard.html')

    def register(self):
        print 'hello'
        info = {
             "first_name" : request.form['first_name'],
             "last_name" : request.form['last_name'],
             "email" : request.form['email'],
             "password" : request.form['password'],
             "pw_confirmation" : request.form['pw_confirm'],
             "dob" : request.form['dob']
        }

        create_status = self.models['User'].register(info)

        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['name'] = create_status['user']['first_name']
            session['message'] = 'Successfully registered!'

            return redirect('/profile/<id>')
        else:
            for message in create_status['errors']:
                flash(message, 'reg_errors')
            return redirect('/')



    def login(self):
        info = {
            "email" : request.form['email'],
            "password" : request.form['password']
        }
        userlogin = self.models['User'].login_user(info)
        if userlogin:
            session['message'] = 'Successfully logged in!'
            session['name'] = userlogin['name']
            session['id'] = userlogin['id']
            return redirect('/profile/<id>')

        elif not userlogin:
            flash('Please enter a valid email and password', 'login_errors')
            return redirect('/')


    def profile(self, id):
        id = session['id']
        user_info = self.models['User'].get_user_id(id)
        events_hosting = self.models['User'].get_events_hosting(id)
        events_attending = self.models['User'].get_events_attending(id)
        return self.load_view('profile.html', events_hosting = events_hosting, events_attending = events_attending, user = user_info[0] )



    def logout(self):
        session.clear()
        return redirect('/')



    def add_message_control(self):
        message_info = {
            'name': request.form['name'],
            'location': request.form['location'],
            'date': request.form['date'],
            'time': request.form['time'],
            'headline': request.form['headline'],
            'message': request.form['message'],
            'host_id': session['id']

        }

        self.models['User'].add_message_model(message_info)
        return self.load_view('dashboard.html')

    def users(self):
        id=session['id']
        user = self.models['User'].get_user_id(id)
        friends = self.models['User'].show_friends(id)
        other_users=self.models['User'].get_other_users(id)
        return self.load_view('users_list.html', user=user[0], friends=friends, other_users=other_users)


    def add_event(self):
        return self.load_view('new_event.html')

    def add_event2(self):
        edata = {
            'name' : request.form['event_name'],
            'date' : request.form['event_date'],
            'location' : request.form['event_location'],
            'description': request.form['event_description'],
            'max': request.form['max_people'],
            'host_id': session['id']
        }
        self.models['User'].add_event2(edata)

        return redirect('/profile')

    def event_description(self,id):
        id = id
        event = self.models['User'].get_event(id)
        attending = self.models['User'].get_attending_people(id)
        return self.load_view('event_description.html', event = event, attending = attending)

    def attend(self,id):
        id = id
        adata = {
            'event_id': id,
            'user_id':session['id']
        }
        attend = self.models['User'].attend(adata)

        return redirect('/event_description/' + id)

    def stop_attend(self,id):
        id = id
        adata = {
            'event_id' : id,
            'user_id': session['id']
        }
        stop_attend = self.models['User'].stop_attend(adata)
        return redirect('/profile')

    def add_friend(self,id):
        id=id
        info = {
            'friend_id':id,
            'user_id': session['id']
        }
        friend = self.models['User'].add_friend_now(info)
        return redirect ('/users')
