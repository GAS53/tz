import os

from pydub import AudioSegment
from flask import current_app

from database import db_func

get_host = os.getenv('FLASK_HOST') if os.getenv('FLASK_HOST') else '0.0.0.0'
get_port = os.getenv('FLASK_PORT') if os.getenv('FLASK_PORT') else 5001



def check_user(user_id, user_token):
    if not user_id:
        return 1, 'пользователя с таким id не существует'
    if not user_token:
        return 1, 'такого токена не существует'
    if user_id == user_token:
        return 0, ''
    return 1, 'у данного пользователя не такой токен'





def check_wav(name: str):
    if name.endswith('.wav'):
        return name.split('.')[0]

def save_file(file, checked_name, user_id):
    print(file, checked_name, user_id)
    file.save()



def check_path(dir_path, file):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    elif os.path.exists(os.path.join(dir_path, file)):
        return True
    return False

def wav_to_mp3(file, user_id):
    name = file.filename
    checked_name = check_wav(name)
    if checked_name:
        checked_name += '.mp3'
        dir_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f'{user_id}')
        is_exist = check_path(dir_path, checked_name)
        if is_exist:
            return 1, 'такой файл уже существует'
        file_path = os.path.join(dir_path, checked_name)
        AudioSegment.from_wav(file).export(file_path, format="mp3")
        res, id_song = db_func.add_to_db(checked_name, user_id)
        if res == 0:
            return 0, id_song
        return 1, id_song
    return 1, 'не подходящий формат файла'


