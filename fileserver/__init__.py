from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import mongoengine

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    MONGODB_URI = 'mongodb://heroku_0fh8tj7n:b5k79gdairee40t58ert2ja4bh@ds259806.mlab.com:59806/heroku_0fh8tj7n'
    mongoengine.connect('heroku_0fh8tj7n',host=MONGODB_URI)
    # mongoengine.connect('heroku_0fh8tj7n',host=os.environ['MONGODB_URI'])
    authentication_policy = AuthTktAuthenticationPolicy('somesecret')
    authorization_policy = ACLAuthorizationPolicy()
    with Configurator(settings=settings,
                      root_factory='.security.FileAccessFactory',
                      authentication_policy=authentication_policy,
                      authorization_policy=authorization_policy) as config:
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()
