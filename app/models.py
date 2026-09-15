from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks_created = db.relationship(
        "Task", foreign_keys="Task.author_id", backref="author", lazy="dynamic"
    )
    tasks_assigned = db.relationship(
        "Task", foreign_keys="Task.assignee_id", backref="assignee", lazy="dynamic"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Task(db.Model):
    STATUS_PENDENTE = "pendente"
    STATUS_ANDAMENTO = "em_andamento"
    STATUS_CONCLUIDA = "concluida"

    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_ANDAMENTO, "Em Andamento"),
        (STATUS_CONCLUIDA, "Concluída"),
    ]

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default=STATUS_PENDENTE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    @property
    def status_label(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def can_edit(self, user):
        return user.is_authenticated and user.id == self.author_id

    def can_update_status(self, user):
        return user.is_authenticated and user.id in (self.author_id, self.assignee_id)

    def __repr__(self):
        return f"<Task {self.title}>"
