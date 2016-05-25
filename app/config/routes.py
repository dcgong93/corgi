from system.core.router import routes

routes['default_controller'] = 'Users'
routes['POST']['/register'] = 'Users#register'
routes['POST']['/login'] = 'Users#login'
routes['/profile'] = 'Users#profile'
routes['/logout'] = 'Users#logout'
routes['/dashboard'] = 'Users#dashboard_control'
routes['POST']['/post_message'] = 'Users#add_message_control'
routes['/events/add'] = 'Users#add_event'
routes['POST']['/events/add/new'] = 'Users#add_event2'
routes['/event_description/<id>'] = 'Users#event_description'
routes['POST']['/event/attend/<id>'] = 'Users#attend'
routes['POST']['/event/stop_attend/<id>'] = 'Users#stop_attend'

