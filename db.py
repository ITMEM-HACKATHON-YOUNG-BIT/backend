from peewee import *


db = SqliteDatabase('example.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = IntegerField(primary_key=True, column_name='user_id')
    first_name = TextField(unique=True, column_name='first_name')
    last_name = TextField(unique=True, column_name='last_name')
    id_telegram = TextField(unique=True, column_name='id_telegram')

    class Meta:
        table_name = 'Users'


# db.connect()
# db.create_tables([Users])

# Users.create(first_name='fname', last_name='lname', id_telegram='idtg')
# print(Users.select().where(Users.first_name == 'fname').get().last_name)

if __name__ == "__main__":
    db.connect()
    db.create_tables([Users])
    db.close()
