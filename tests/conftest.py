import pytest

from app import create_app, db
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, username="ana", email="ana@example.com", password="senha123"):
    return client.post(
        "/register",
        data={
            "username": username,
            "email": email,
            "password": password,
            "password2": password,
        },
        follow_redirects=True,
    )


def login(client, email="ana@example.com", password="senha123"):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )
