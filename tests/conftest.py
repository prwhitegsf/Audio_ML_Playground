import pytest

from app import create_app, db as _db
import app.src.models as model
import sqlalchemy as sa
from sqlalchemy.orm import Session
from config import TestConfig
import os


@pytest.fixture(scope='session')
def app():
  
    app = create_app(config_class=TestConfig)
  

    yield app


@pytest.fixture(scope='session')
def app_ctx(app):
    with app.app_context():
        yield



@pytest.fixture(scope='session')
def db(app, app_ctx):
	_db.app = app
	_db.create_all()

	yield _db

	_db.drop_all()


@pytest.fixture(scope='function')
def session(app, db, app_ctx):

    connection = db.engine.connect()
    transaction = connection.begin()

    session = db._make_scoped_session(options={'bind': connection})
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
    
    '''
    model.db.app = app
    model.db.create_all()

    engine = sa.create_engine("sqlite+pysqlite:///tester.db")
    session = Session(engine)

    yield session

    session.close()
    model.db.drop_all()
    '''
