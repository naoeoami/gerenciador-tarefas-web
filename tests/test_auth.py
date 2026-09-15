from app.models import User
from tests.conftest import login, register


def test_register_creates_user(app, client):
    response = register(client)
    assert response.status_code == 200

    with app.app_context():
        assert User.query.filter_by(email="ana@example.com").first() is not None


def test_register_duplicate_email_fails(app, client):
    register(client)
    response = register(client, username="outra")
    assert b"j\xc3\xa1 est\xc3\xa1 cadastrado" in response.data

    with app.app_context():
        assert User.query.count() == 1


def test_login_with_valid_credentials(client):
    register(client)
    response = login(client)
    assert response.status_code == 200
    assert b"Dashboard do Grupo" in response.data


def test_login_with_invalid_password_fails(client):
    register(client)
    response = login(client, password="senha-errada")
    assert b"inv\xc3\xa1lidos" in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=True)
    assert b"Fa\xc3\xa7a login" in response.data


def test_logout(client):
    register(client)
    login(client)
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Entrar" in response.data
