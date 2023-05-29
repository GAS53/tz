import os

from flask import Flask, request, current_app, send_from_directory
from werkzeug.utils import secure_filename

from database import db_func, base
import utils

app = Flask(__name__)

db_path = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postge_db:5432/{os.getenv('POSTGRES_DB')}" if os.getenv('POSTGRES_USER') else "sqlite://///home/main/Documents/bewise.ai/sqllite.db"

app.config['MAX_CONTENT_LENGTH'] = 1000024
app.config['UPLOAD_FOLDER'] = f'{os.getcwd()}/uploads'
app.config["SQLALCHEMY_DATABASE_URI"] = db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
ALLOWED_EXTENSIONS = set(['wav'])


base.db.init_app(app)


@app.errorhandler(404)
def handler_404(error):
    app.logger.error(error)
    return 'нет такой страници 404'



@app.post('/add_user/<string:val>')
def add_user(val: str):
    res, description = db_func.add(val)
    if res == 0:
        return description, 200
    return {'db error': description}, 500

@app.post('/upload')
def upload_file():
    msg = 'error'
    if request.method == 'POST':
        token_u = db_func.get_user(request.form["token"], is_id=False)
        id_u = db_func.get_user(request.form["user_id"])
        res, msg = utils.check_user(user_token=token_u, user_id=id_u)
        if res == 0:
            if 'file' in request.files:
                file = request.files['file']
                res, msg = utils.wav_to_mp3(file, id_u.id )
                if res == 0:
                    return f'http://{utils.get_host}:{utils.get_port}/record?song_id={msg}&user_id={id_u.id}'
    return msg, 500


@app.get('/record')
def record():
    song_id = request.args.get('song_id')
    user_id = request.args.get('user_id')
    res, song = db_func.get_song(song_id, user_id)
    if res == 0:
        directory = os.path.join(current_app.config['UPLOAD_FOLDER'], f'{song.user_id}')
        file_exists = utils.check_path(directory, song.name)
        if not file_exists:
            return 'файла не существует в базе/повреждено файловое хранилище', 500
        return send_from_directory(directory=directory, path=song.name)
    return song, 500