from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

import os

app = Flask(__name__, static_folder='static')
#Secret key encrypts user sessions
app.secret_key = os.urandom(24)
app.config['OAUTH_CREDENTIALS'] = {
        'facebook' : {
            'id':'248359842587200',
            'secret': 'd8743f2761e5f4ae94331d09bee1608c'
            },
        'twitter' : {
            'id': 'EPfVG84v3v4cUMBMD1LpKoe8b',
            'secret': 'qHZ5P0bZJukrioVsBxHuS7NfLWixxBMnwKJlZILqXuogypN8G8'
            }
        }
app.config.from_object(Config)

#Instantiating database - Adding a db object + migration engine object
db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view='index'
migrate = Migrate(app, db)

#Implement Cache Buster in __init__
@app.context_processor
def overrider_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)



from app import routes, models
