# views.py


from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm, AddStataForm
from sqlalchemy.exc import IntegrityError
import datetime


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import User, Stata

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login!')
			return redirect(url_for('login'))
	return wrap

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')

# Log Out
@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('You are successfully logged out')
	return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User.query.filter_by(
                name=request.form['name'],
                password=request.form['password']
            ).first()
            if u is None:
                error = 'Invalid username or password.'
                return render_template(
                    "login.html",
                    form=form,
                    error=error
                )
            else:
                session['logged_in'] = True
                session['user_id'] = u.id
                flash('Successfully logged in.')
                return redirect(url_for('main'))
        else:
            return render_template(
                "login.html",
                form=form,
                error=error
            )
    if request.method == 'GET':
        return render_template('login.html', form=form)

# User Registration:
@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data,
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thank you for registering. You may log in.')
                return redirect(url_for('login'))
            except IntegrityError:
                error = 'This username or email already exist. Please try another one.'
                return render_template('register.html', form = form, error = error)
        else:
            return render_template('register.html', form = form, error = error)
    if request.method == 'GET':
        return render_template('register.html', form = form)


# stata enter
@app.route('/stat_submit/', methods = ['GET', 'POST'])
@login_required
def stat_submit():
    form = AddStataForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            x = "what the ffff"
            # parse form.body.data here
            new_stata = Stata(
                x,
                #form.body.data,
                datetime.datetime.utcnow(),
                session['user_id']
                )
            db.session.add(new_stata)
            db.session.commit()
            flash('ZAYEBESS')
            return redirect(url_for('statistics'))
        else:
            flash('PIZDETS')
            return redirect(url_for('stat_submit'))
    return render_template('stat_submit.html', form = form)




# main - empty for now
@app.route('/main')
@login_required
def main():
    return render_template('main.html')


# teamspeak viewer
@app.route('/teamspeak/')
@login_required
def teamspeak():
    return render_template('teamspeak.html')



@app.route('/progress/')
@login_required
def progress():
    return render_template('progress.html')


@app.route('/statistics')
@login_required
def statistics():
    return render_template('statistics.html')


@app.route('/teamspeak2')
@login_required
def teamspeak2():
    return render_template('teamspeak2.html')