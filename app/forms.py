from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import Task, User


class RegistrationForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        "Confirmar Senha",
        validators=[DataRequired(), EqualTo("password", message="As senhas devem ser iguais.")],
    )
    submit = SubmitField("Cadastrar")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Este nome de usuário já está em uso.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Este e-mail já está cadastrado.")


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class TaskForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(max=140)])
    description = TextAreaField("Descrição", validators=[Length(max=2000)])
    status = SelectField("Status", choices=Task.STATUS_CHOICES, validators=[DataRequired()])
    assignee_id = SelectField("Atribuir a", coerce=int)
    submit = SubmitField("Salvar")
