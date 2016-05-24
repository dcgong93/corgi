from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db

    def index(self):

        return self.load_view('index.html')

    def dashboard_control(self):
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

            return redirect('/profile')
        else:
            for message in create_status['errors']:
                flash(message, 'reg_errors')
            return redirect('/')

    def profile(self):
        return self.load_view('profile.html')

    def login(self):
        info = {
            "email" : request.form['email'],
            "password" : request.form['password']
        }
        userlogin = self.models['User'].login_user(info)
        if userlogin:
            session['message'] = 'Successfully logged in!'
            session['name'] = userlogin
            session['id'] = userlogin['id']
            return redirect('/profile')

        elif not userlogin:
            flash('Please enter a valid email and password', 'login_errors')
            return redirect('/')


    def logout(self):
        session.clear()
        return redirect('/')

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

        return redirect('/dashboard')
