from app.models import Task, User
from tests.conftest import login, register


def create_task(client, title="Minha tarefa", status="pendente", assignee_id=0):
    return client.post(
        "/tasks/new",
        data={
            "title": title,
            "description": "descrição de teste",
            "status": status,
            "assignee_id": assignee_id,
        },
        follow_redirects=True,
    )


def test_create_task(app, client):
    register(client)
    login(client)
    response = create_task(client)
    assert response.status_code == 200

    with app.app_context():
        task = Task.query.filter_by(title="Minha tarefa").first()
        assert task is not None
        assert task.status == "pendente"


def test_edit_task_by_author(app, client):
    register(client)
    login(client)
    create_task(client)

    with app.app_context():
        task = Task.query.first()

    response = client.post(
        f"/tasks/{task.id}/edit",
        data={
            "title": "Tarefa atualizada",
            "description": "nova descrição",
            "status": "em_andamento",
            "assignee_id": 0,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        updated = Task.query.get(task.id)
        assert updated.title == "Tarefa atualizada"
        assert updated.status == "em_andamento"


def test_other_user_cannot_edit_task(app, client):
    register(client, username="ana", email="ana@example.com")
    login(client, email="ana@example.com")
    create_task(client)

    with app.app_context():
        task = Task.query.first()

    client.get("/logout")
    register(client, username="bruno", email="bruno@example.com")
    login(client, email="bruno@example.com")

    response = client.get(f"/tasks/{task.id}/edit")
    assert response.status_code == 403


def test_delete_task(app, client):
    register(client)
    login(client)
    create_task(client)

    with app.app_context():
        task = Task.query.first()

    client.post(f"/tasks/{task.id}/delete", follow_redirects=True)

    with app.app_context():
        assert Task.query.count() == 0


def test_status_filter_on_dashboard(client):
    register(client)
    login(client)
    create_task(client, title="Tarefa pendente", status="pendente")
    create_task(client, title="Tarefa concluída", status="concluida")

    response = client.get("/dashboard?status=concluida")
    assert b"Tarefa conclu\xc3\xadda" in response.data
    assert b"Tarefa pendente" not in response.data
