from peewee import *

sqlite_db = SqliteDatabase('my_database')

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database =sqlite_db

class User(BaseModel):
    username = CharField()


sqlite_db.connect()
sqlite_db.create_tables([BaseModel,User])
