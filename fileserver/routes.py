def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('upload', '/upload')
    config.add_route('login','/login')
    config.add_route('register','/register')
    config.add_route('logout','/logout')
    config.add_route('userfiles','/myfiles')
    config.add_route('preview','/p{file_id}')
    config.add_route('download','/d{file_id}')
    config.add_route('delete','/x{file_id}')

