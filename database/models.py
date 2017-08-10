from peewee import Model, CharField, IntegerField
from playhouse.db_url import connect
DB_LINK = 'mysql://root:magpies666@94.246.168.27:3306/tn'
db = connect(DB_LINK)

class BaseModel(Model):
    class Meta:
        database = db


class Input(BaseModel):
    name = CharField(50)
    number = IntegerField()