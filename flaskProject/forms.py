from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateTimeField, FloatField
from wtforms.validators import DataRequired, Email, InputRequired
from wtforms.fields.html5 import DateField, TimeField


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[InputRequired("Please enter your email address."),
                                    Email("This field requires a valid email address")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class PostExpense(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category',
                           choices=[('Groceries', 'Groceries'), ('Utilities', 'Utilities'), ('Housing', 'Housing')],
                           validators=[DataRequired()])
    datetime = DateField('Date')
    time = TimeField('Time')
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add')
