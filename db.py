from peewee import *
from pprint import pprint


db = SqliteDatabase('example.sqlite')


class BaseModelDB(Model):
    class Meta:
        database = db


class Users(BaseModelDB):
    user_id = IntegerField(primary_key=True, column_name='user_id')
    first_name = TextField(column_name='first_name')
    second_name = TextField(column_name='second_name')
    third_name = TextField(column_name='third_name', null=True)
    user_tg_id = BigIntegerField(column_name='user_tg_id', null=True)
    username_tg = TextField(column_name='username_tg', null=True)
    user_site_id = BigIntegerField(unique=True, column_name='user_site_id', null=True)
    birthday = TextField(column_name='birthday')
    sex = TextField(column_name='sex')
    phone = TextField(column_name='phone', null=True)
    email = TextField(column_name='email', null=True)
    region = TextField(column_name='region', null=True)

    class Meta:
        table_name = 'Users'


class Events(BaseModelDB):
    _id = IntegerField(primary_key=True, column_name='_id')
    event_id = TextField(unique=True, column_name='event_id', null=True)
    name = TextField(column_name='name', null=True)
    organizerName = TextField(column_name='organizerName', null=True)
    region = TextField(column_name='region', null=True)
    eventType = TextField(column_name='eventType', null=True)
    ageFrom = BigIntegerField(column_name='ageFrom', null=True)
    ageTo = BigIntegerField(column_name='ageTo', null=True)
    beginsAt = DateTimeField(column_name='beginsAt', null=True)
    endsAt = DateTimeField(column_name='endsAt', null=True)
    registrationBeginsAt = DateTimeField(column_name='registrationBeginsAt', null=True)
    registrationEndsAt = DateTimeField(column_name='registrationEndsAt', null=True)
    url = TextField(column_name='url', null=True)
    timestamp = DateTimeField(column_name='timestamp')

    class Meta:
        table_name = 'Events'


class Admins(BaseModelDB):
    admin_id = IntegerField(primary_key=True, column_name='admin_id')
    name = TextField(column_name='name', null=True)
    admin_tg_id = BigIntegerField(column_name='admin_tg_id')


# db.connect()
# db.create_tables([Users])

# Users.create(first_name='fname', last_name='lname', id_telegram='idtg')
# print(Users.select().where(Users.first_name == 'fname').get().last_name)

def create_database():
    db.connect()
    db.create_tables([Users, Events, Admins])
    db.close()
    Admins.create(name="Максим", admin_tg_id=664892538)


def add_users():
    Users.create(**{"first_name": "q",
                    "second_name": "w",
                    "third_name": "e",
                    "user_tg_id": 123,
                    "username_tg": "t",
                    "user_site_id": 2345,
                    "birthday": "u",
                    "sex": "i",
                    "phone": "o",
                    "email": "p",
                    "region": "["})


def print_db(table):
    pprint(list(table.select().dicts()))


if __name__ == "__main__":
    # create_database()
    # add_users()
    print_db(Users)
    print_db(Events)
    # pprint(vars(Events))
    # print(type(list(Users.select().dicts())[0]))
    # for i in Users.select():
    #     print(i.user_id)
