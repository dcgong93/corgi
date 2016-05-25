from system.core.router import routes

routes['default_controller'] = 'Users'
routes['POST']['/register'] = 'Users#register'
routes['POST']['/login'] = 'Users#login'
routes['/profile'] = 'Users#profile'
routes['/logout'] = 'Users#logout'
routes['/users/<id>'] = 'Users#users'
routes['/events/add'] = 'Users#add_event'
routes['POST']['/events/add/new'] = 'Users#add_event2'
