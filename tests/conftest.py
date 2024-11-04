# tests/conftest.py

import pytest
from app import create_app, db as _db
from app.models import Department, Collaborator
from .test_conf import TestConfig


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.from_object(TestConfig)

    with app.app_context():
        _db.create_all()

    yield app

    with app.app_context():
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database():
    pass
