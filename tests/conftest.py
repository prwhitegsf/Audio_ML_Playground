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


@pytest.fixture()
def client(app):
    return app.test_client()
