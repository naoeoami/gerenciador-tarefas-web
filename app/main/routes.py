from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.models import Task

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    status = request.args.get("status")
    valid_statuses = {choice for choice, _ in Task.STATUS_CHOICES}

    query = Task.query
    if status in valid_statuses:
        query = query.filter(Task.status == status)
    tasks = query.order_by(Task.created_at.desc()).all()

    counts = {choice: Task.query.filter_by(status=choice).count() for choice, _ in Task.STATUS_CHOICES}
    counts["total"] = Task.query.count()

    return render_template(
        "main/dashboard.html",
        tasks=tasks,
        status_choices=Task.STATUS_CHOICES,
        current_status=status,
        counts=counts,
    )
