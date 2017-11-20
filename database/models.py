from config import Config
import datetime
from peewee import Model, CharField, IntegerField, ForeignKeyField, DateTimeField, BooleanField
from playhouse.db_url import connect

DB_LINK = Config.db_link
db = connect(DB_LINK)


class BaseModel(Model):
    class Meta:
        database = db


class Input(BaseModel):
    name = CharField(50)
    number = IntegerField()


class InputState(BaseModel):
    input = ForeignKeyField(Input, related_name='states')
    datetime = DateTimeField(default=datetime.datetime.now)
    state = BooleanField(default=False)
