from app import app
from database.base import db
from utils import get_host, get_port

@app.cli.command('init_db')
def init_db():
    db.create_all()



if __name__== '__main__':
    app.run(host=get_host, debug=False, port=get_port)