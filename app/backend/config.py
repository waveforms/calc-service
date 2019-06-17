import os

basedir = os.path.abspath(os.path.dirname(__file__))


USER = 'root'
PASS = 'root'
HOST = "127.0.0.1"
DB = 'knights'
PORT = '32000'
URI = f'mysql+mysqlconnector://{USER}:{PASS}@{HOST}:{PORT}/{DB}'

class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = "\2\1thisismyscretkey\1\2\e\y\y\h"


    #SQLALCHEMY_DATABASE_URI = URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")