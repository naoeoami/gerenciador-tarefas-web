from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db
from app.forms import TaskForm
from app.models import Task, User

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def assignee_choices():
    users = User.query.order_by(User.username).all()
    return [(0, "Ninguém")] + [(u.id, u.username) for u in users]


def valid_statuses():
    return {choice for choice, _ in Task.STATUS_CHOICES}


@tasks_bp.route("/")
@login_required
def list_tasks():
    status = request.args.get("status")
    query = Task.query.filter(
        or_(Task.author_id == current_user.id, Task.assignee_id == current_user.id)
    )
    if status in valid_statuses():
        query = query.filter(Task.status == status)

    tasks = query.order_by(Task.created_at.desc()).all()
    return render_template(
        "tasks/list.html", tasks=tasks, status_choices=Task.STATUS_CHOICES, current_status=status
    )


@tasks_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_task():
    form = TaskForm()
    form.assignee_id.choices = assignee_choices()

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            author_id=current_user.id,
            assignee_id=form.assignee_id.data or None,
        )
        db.session.add(task)
        db.session.commit()
        flash("Tarefa criada com sucesso.", "success")
        return redirect(url_for("tasks.list_tasks"))

    return render_template("tasks/form.html", form=form, title="Nova Tarefa")


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    if not task.can_edit(current_user):
        abort(403)

    form = TaskForm(obj=task)
    form.assignee_id.choices = assignee_choices()

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.assignee_id = form.assignee_id.data or None
        db.session.commit()
        flash("Tarefa atualizada com sucesso.", "success")
        return redirect(url_for("tasks.list_tasks"))

    if request.method == "GET":
        form.assignee_id.data = task.assignee_id or 0

    return render_template("tasks/form.html", form=form, title="Editar Tarefa", task=task)


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    if not task.can_edit(current_user):
        abort(403)

    db.session.delete(task)
    db.session.commit()
    flash("Tarefa excluída.", "info")
    return redirect(request.referrer or url_for("tasks.list_tasks"))


@tasks_bp.route("/<int:task_id>/status", methods=["POST"])
@login_required
def update_status(task_id):
    task = db.get_or_404(Task, task_id)
    if not task.can_update_status(current_user):
        abort(403)

    new_status = request.form.get("status")
    if new_status not in valid_statuses():
        flash("Status inválido.", "danger")
    else:
        task.status = new_status
        db.session.commit()
        flash("Status atualizado.", "success")

    return redirect(request.referrer or url_for("tasks.list_tasks"))
