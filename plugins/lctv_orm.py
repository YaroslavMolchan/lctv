from peewee import *
import datetime

db = SqliteDatabase('/home/molchan/www/lctv/storage/lctv.db', threadlocals=True)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    views = IntegerField(default=1)
    is_vip = BooleanField(default=False)
    is_online = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)

class Songs(BaseModel):
    id = CharField(unique=True)
    artist = CharField()
    name = CharField()
    requests = IntegerField(default=1)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Songs, self).save(*args, **kwargs)

class SongsSearch(BaseModel):
    username = CharField()
    requested_name = TextField()
    requested_limit = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

# class Tweet(BaseModel):
#     user = ForeignKeyField(User, related_name='tweets')
#     message = TextField()
#     created_date = DateTimeField(default=datetime.datetime.now)
#     is_published = BooleanField(default=True)

# db.connect()
# db.create_tables([User, Songs, SongsSearch])