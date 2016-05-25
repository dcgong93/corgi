from system.core.router import routes

routes['default_controller'] = 'Users'
routes['POST']['/register'] = 'Users#register'
routes['POST']['/login'] = 'Users#login'
routes['/profile'] = 'Users#profile'
routes['/logout'] = 'Users#logout'
routes['/dashboard'] = 'Users#dashboard_control'
routes['POST']['/post_message'] = 'Users#add_message_control'

