from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateTimeField, FloatField
from wtforms.validators import DataRequired, Email, InputRequired


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[InputRequired("Please enter your email address."),
                                    Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class PostExpense(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category',
                           choices=[('text', 'Groceries'), ('text', 'Utilities'), ('text', 'Housing')],
                           validators=[DataRequired()])
    datetime = DateTimeField('Date')
    ammount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add')
