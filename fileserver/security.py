from pyramid.security import Allow, Everyone, Authenticated


class FileAccessFactory(object):
    __acl__ = [(Allow, Everyone, 'basic'),
               (Allow, Authenticated, 'manage'),]

    def __init__(self, request):
        pass