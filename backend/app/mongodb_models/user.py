from mongoengine import Document, StringField, BooleanField, IntField, ListField, ReferenceField, EmailField, LongField
from mongoengine import NULLIFY, PULL


class User(Document):
    ID = LongField(unique=True, required=True)
    Username = StringField(required=True)
    Password = StringField()
    IsLock = BooleanField(required=True)

