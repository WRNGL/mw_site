# views.py


from flask import Flask, flash, redirect, render_template, request, session, url_for
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm, AddStataForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text, select, func
from statparser import Statz
import datetime, requests
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from models import User, Stata

##########################
#### helper functions ####
##########################

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

def profile_stat():
    user_id = session['user_id']
    return db.session.query(Stata).filter_by(user_id=user_id).order_by(Stata.stata_id.desc()).limit(1)

def total_kills():
    inn = db.session.query(Stata).filter(Stata.user_id, Stata.kills, Stata.stata_id).group_by(Stata.user_id).subquery()
    return db.session.query(func.sum(inn.columns.kills)).scalar()

def total_deaths():
    inn = db.session.query(Stata).filter(Stata.user_id, Stata.deaths, Stata.stata_id).group_by(Stata.user_id).subquery()
    return db.session.query(func.sum(inn.columns.deaths)).scalar()

def total_wins():
    inn = db.session.query(Stata).filter(Stata.user_id, Stata.wins, Stata.stata_id).group_by(Stata.user_id).subquery()
    return db.session.query(func.sum(inn.columns.wins)).scalar()

def total_losses():
    inn = db.session.query(Stata).filter(Stata.user_id, Stata.losses, Stata.stata_id).group_by(Stata.user_id).subquery()
    return db.session.query(func.sum(inn.columns.losses)).scalar()

def total_cbills():
    inn = db.session.query(Stata).filter(Stata.user_id, Stata.cbills, Stata.stata_id).group_by(Stata.user_id).subquery()
    return db.session.query(func.sum(inn.columns.cbills)).scalar()

    
    
    # sum = SELECT sum(kills) FROM stata t1 WHERE stata_id = (SELECT max(stata_id) FROM stata WHERE t1.user_id = stata.user_id) ORDER BY stata_id DESC
    # return db.session.query(Stata).filter_by(user_id=user_id).order_by(Stata.stata_id.asc())

    # latest record = select kills from stata order by stata_id desc limit 1

    #return db.session.query(Stata).filter(user_id=user_id, stata_id).order_by(func.max(Stata.stata_id))

    #return db.session.query(Stata).filter(user_id, func.max(stat_id))  
    #   SELECT kills FROM stata where user_id = '1' and stata_id = (SELECT MAX(stata_id)  FROM stata);
    #   return db.session.query(Stata).filter_by(user_id='1', stata_id=func.max(Stata.stata_id))  
    #
    #   working query:
    #   select sum(kills) from
    #   (select user_id, kills , max(stata_id)
    #   from stata
    #   group by user_id);

def top_users_kills():
    #return db.session.query(Stata.kills).group_by(Stata.user_id).all()
    return db.session.query(Stata.user_id, User.name).group_by(Stata.user_id).join(User).order_by(Stata.kills.desc())


    
    
    # select max(kills) from stata group by user_id;
    #
    # LIMIT 1 OFFSET 3;
    # select name, max(kills) as jew from
    # (SELECT users.name, stata.mc, stata.kills, stata.deaths, stata.cbills, stata.exp_points, stata.wins,
    # stata.losses
    # FROM stata
    # INNER JOIN users
    # ON stata.user_id=users.id)
    # group by name order by jew desc;;


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
                bcrypt.generate_password_hash(form.password.data)
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


# User login:
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User.query.filter_by(name=request.form['name']).first()
            if u is not None and bcrypt.check_password_hash(u.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = u.id
                session['name'] = u.name
                flash('Successfully logged in.')
                return redirect(url_for('main'))
            else:
                error = 'Invalid username or password.'   
    return render_template('login.html', form=form, error=error)


# Log Out
@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You are successfully logged out')
    return redirect(url_for('login'))


# stata enter
@app.route('/stat_submit/', methods = ['GET', 'POST'])
@login_required
def stat_submit():
    form = AddStataForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            stat_data = form.body.data
            mc = Statz(stat_data)[0]
            kills = Statz(stat_data)[1]
            deaths = Statz(stat_data)[2]
            cbills = Statz(stat_data)[3]
            exp_points = Statz(stat_data)[4]
            wins = Statz(stat_data)[5]
            losses = Statz(stat_data)[6]
            new_stata = Stata(
                mc,
                kills,
                deaths,
                cbills,
                exp_points,
                wins,
                losses,
                datetime.datetime.utcnow(),
                session['user_id']
                )
            db.session.add(new_stata)
            db.session.commit()
            flash('Stats added successfully')
            return redirect(url_for('stat_submit'))
        else:
            flash('Validation failed')
            return redirect(url_for('stat_submit'))
    return render_template('stat_submit.html', form = form, username = session['name'])


@app.route('/profile')
@login_required
def profile():
    return render_template(
        'profile.html',
        username = session['name'],
        profile_stat = profile_stat()
        )


@app.route('/statistics')
@login_required
def statistics():
    return render_template(
        'statistics.html',
        username = session['name'],
        total_kills = total_kills(),
        total_deaths = total_deaths(),
        total_wins = total_wins(),
        total_losses = total_losses(),
        total_cbills = total_cbills(),
        tk = top_users_kills()
        )

# main - empty for now
@app.route('/main')
@login_required
def main():
    return render_template('main.html',
        username = session['name'])


# teamspeak viewer
@app.route('/teamspeak/')
@login_required
def teamspeak():
    return render_template('teamspeak.html',
        username = session['name'])


@app.route('/progress/')
@login_required
def progress():
    return render_template('progress.html',
        username = session['name'])



@app.route('/teamspeak2')
@login_required
def teamspeak2():
    return render_template('teamspeak2.html',
        username = session['name'])