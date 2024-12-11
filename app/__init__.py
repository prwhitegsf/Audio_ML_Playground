import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os
from flask import Flask, request, current_app
from config import Config

import app.src.models as model


def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

class Base(DeclarativeBase):
  pass


db = model.db



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    #print(app.url_map)

    db.init_app(app)

    

    if not app.debug and not app.testing:


        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/test.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('test startup')

    return app


#from app import models