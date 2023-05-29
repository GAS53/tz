from uuid import uuid4

from sqlalchemy import Column, Integer, String, Uuid, ForeignKey

from database.base import db

class Song(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(36))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f'song {self.name}, song creater id {self.user_id}'




class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(36), unique=True)
    uuid = Column(Uuid(as_uuid=True), unique=True, default=uuid4)
    songs = db.relationship(Song, backref='user')

    def __repr__(self):
        return f'name {self.name}, id {self.id} uuid {self.uuid}'
    

