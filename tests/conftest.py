import pytest

from app import create_app
import app.src.models as model
import sqlalchemy as sa
from sqlalchemy.orm import Session

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING":True,
        'SQLALCHEMY_DATABASE_URI':"sqlite+pysqlite:///tester.db"
    })

    yield app


@pytest.fixture(scope='session')
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture(scope='session')
def db(app, app_ctx):
    engine = sa.create_engine("sqlite+pysqlite:///tester.db")
    model.db.app = app
    model.db.create_all()

    yield model.db

    model.db.drop_all()

@pytest.fixture(scope='function')
def session(app, db, app_ctx):
    engine = sa.create_engine("sqlite+pysqlite:///tester.db")
    #connection = db.engine.connect()
    #transaction = connection.begin()

    session = Session(engine)

    yield session

    session.close()
     
