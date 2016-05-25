from system.core.router import routes

routes['default_controller'] = 'Users'
routes['POST']['/register'] = 'Users#register'
routes['POST']['/login'] = 'Users#login'
routes['/profile/<id>'] = 'Users#profile'
routes['/logout'] = 'Users#logout'
routes['/users/'] = 'Users#users'
routes['/events/add'] = 'Users#add_event'
routes['POST']['/events/add/new'] = 'Users#add_event2'
routes['/event_description/<id>'] = 'Users#event_description'
