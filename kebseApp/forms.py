from flask_wtf import Form, FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('email',
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField('password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('confirm password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('sign Up')
