from flaskProject import app, db
from flask import render_template, flash, redirect, url_for, request, abort
from flaskProject.forms import LoginForm, PostExpense
from flask_login import login_user, current_user, logout_user, login_required
from flaskProject.models import User, Expense
import datetime, json


def format_date():
    date_time_str = f"{request.form.get('date')} {request.form.get('time')}:00.000000"
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
    return date_time_obj


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
        expense1 = Expense(description=form.description.data,
                           category=form.category.data,
                           amount=float(request.form.get('amount')),
                           date_expense=format_date(),
                           user=current_user)
        db.session.add(expense1)
        db.session.commit()
        flash('Your expense has been added', 'success')
        return redirect(url_for('home'))

    return render_template('create_expense.html',
                           title='New expense',
                           date='',
                           time='',
                           amount='',
                           legend='New expense',
                           form=form)


@app.route('/expense/<int:expense_id>')
def expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    return render_template('expense.html', title=expense.id, expense=expense)


@app.route('/expense/<int:expense_id>/update', methods=['GET', 'POST'])
@login_required
def expense_update(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if expense.user != current_user:
        abort(403)
    form = PostExpense()
    if form.validate_on_submit():
        expense.description = form.description.data
        expense.category = form.category.data
        expense.date_expense = format_date()
        expense.amount = float(request.form.get('amount'))
        db.session.commit()
        flash('Your expense has been updated!', 'success')
        return redirect(url_for('expense', expense_id=expense.id))
    elif request.method == 'GET':
        form.description.data = expense.description
        form.category.data = expense.category
        date = expense.date_expense.date()
        time = datetime.datetime.strftime(expense.date_expense, "%H:%M")
        amount = expense.amount
    return render_template('create_expense.html',
                           title='New expense',
                           legend='Edit expense',
                           date=date,
                           time=time,
                           amount=amount,
                           form=form)


@app.route('/expense/<int:expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user != current_user:
        abort(403)
    db.session.delete(expense)
    db.session.commit()
    flash('Your expense has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/report/')
@login_required
def get_report():
    if current_user.is_authenticated:
        user = User.query.filter_by(email=current_user.email).first()
        expenses = user.expenses
        print(expenses)
        print(type(expenses))
        return render_template('report.html', expenses=expenses)
    else:
        return render_template('report.html')
