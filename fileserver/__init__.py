from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import mongoengine
import os

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # mongoengine.connect('heroku_0fh8tj7n',host=MONGODB_URI)
    mongoengine.connect('heroku_0fh8tj7n',host=os.environ['MONGODB_URI'])
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
