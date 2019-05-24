import unittest
import mongoengine

from pyramid import testing

MONGODB_URI = 'mongodb://heroku_0fh8tj7n:b5k79gdairee40t58ert2ja4bh@ds259806.mlab.com:59806/heroku_0fh8tj7n'
mongoengine.connect('heroku_0fh8tj7n',host=MONGODB_URI)

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views.default import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'test')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from fileserver import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Pyramid' in res.body)
