from flaskProject import app
from flask import render_template, flash, redirect, url_for, request, abort
from flaskProject.forms import LoginForm, PostExpense
from flask_login import login_user, current_user, logout_user, login_required
from flaskProject.models import User, Expense


@app.route('/')
@app.route('/home', )
def home():
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
        expenses = user.expenses
        return render_template('home.html', expenses=expenses)
    else:
        return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = User.query.filter_by(password=form.password.data).first()
        if user and password:
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/expense/new', methods=['GET', 'POST'])
@login_required
def new_expense():
    form = PostExpense()
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_expense.html', title='New expense', form=form)


@app.route('/expense/<int:expense_id>')
def expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    return render_template('expense.html', title=expense.id, expense=expense)


@app.route('/expense/<int:expense_id>/update')
@login_required
def expense_update(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user != current_user:
        abort(403)