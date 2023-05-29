import uuid

from sqlalchemy.exc import IntegrityError

from database.base import db
from database.models import User, Song

def add(name):
    try:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return 0, {'id': user.id, 'uuid': user.uuid}
    except IntegrityError:
        return 1, 'name not unic'
    except Exception as e:
        return 1, e


def add_to_db(song, user_id):
    try:
        song = Song(user_id=user_id, name=song)
        db.session.add(song)
        db.session.commit()
        return 0, song.id
    except Exception as e:
        return 1, e
        


def get_user(input_id, is_id=True):
    if input_id:
        if is_id:
            usr = User.query.filter_by(id=input_id).first()
        else:
            input_id = uuid.UUID(input_id)
            usr = User.query.filter_by(uuid=input_id).first()
        if usr:
            return usr
    return False

def get_song(song_id, user_id):
    song = db.session.query(Song).filter_by(user_id=user_id, id=song_id).first()
    print(f'song {song}')
    if song:
        return 0, song
    return 1, 'нет такой песни'