import orm_sqlite


class User(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)  # auto-increment
    login = orm_sqlite.StringField()
    id_telegram = orm_sqlite.StringField()



