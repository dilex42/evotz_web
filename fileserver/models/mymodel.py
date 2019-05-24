from mongoengine import *
from passlib.apps import custom_app_context
import datetime
# Create your models here.

class MetaInfo(Document) :
    next_check = DateTimeField(default=datetime.datetime.now)

class Users(Document) :
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    def set_password(self, password):
        password_hash = custom_app_context.encrypt(password)
        self.password = password_hash

    @classmethod
    def by_name(cls, name):
        return cls.objects(username = name).first()

class Files(Document) :
    user = ReferenceField(Users)
    file = FileField()
    expires_at = DateTimeField(required=True)
    description = StringField(default='No Description')

