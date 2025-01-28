from mongoengine import DynamicDocument, StringField, EmailField, \
BooleanField, DateTimeField, ListField, EmbeddedDocumentField, EmbeddedDocument
from datetime import datetime

class Message(EmbeddedDocument):
    created_at = DateTimeField()
    content = StringField()
    role = StringField()



class User(DynamicDocument):
    created_at = DateTimeField()
    updated_at = DateTimeField()
    messages = ListField(EmbeddedDocumentField(Message))


