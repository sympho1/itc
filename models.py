import peewee

db_recette = peewee.SqliteDatabase('recette.db')


class BaseModel(peewee.Model):
    class Meta:
        database = db_recette


class Cuisto(BaseModel):
    name = peewee.CharField()
    phone = peewee.CharField()
    photo = peewee.CharField()


class Recette(BaseModel):
    owner = peewee.ForeignKeyField(Cuisto, related_name='recettes')
    title = peewee.CharField()
    ingredient = peewee.TextField()
    preparation = peewee.TextField()
    posted = peewee.DateTimeField()