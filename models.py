# models.py
import datetime
from views import db



class User(db.Model):
	__tablename__ = 'users'
	__table_args__ = {'sqlite_autoincrement': True}

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, unique = True, nullable = False)
	email = db.Column(db.String, unique = True, nullable = False)
	password = db.Column(db.String, nullable = False)
	is_member = db.Column(db.String)

	def __init__(self, name = None, email = None, password = None, is_member = None):
		self.name = name
		self.email = email
		self.password = password
		self.is_member = is_member

	def __repr__(self):
		return '<User %r>' % (self.name)

class Stata(db.Model):
	__tablename__ = 'stata'
	stata_id = db.Column(db.Integer, primary_key = True)
	mc = db.Column(db.Integer)
	kills = db.Column(db.Integer)
	deaths = db.Column(db.Integer)
	cbills = db.Column(db.Integer)
	exp_points = db.Column(db.Integer)
	wins = db.Column(db.Integer)
	losses = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __init__(self, mc, kills, deaths, cbills, exp_points, wins, losses, timestamp, user_id):
		self.mc = mc
		self.kills = kills
		self.deaths = deaths
		self.cbills = cbills
		self.exp_points = exp_points
		self.wins = wins
		self.losses = losses
		self.timestamp = timestamp
		self.user_id = user_id

	def __repr__(self):
		return '<Post %r>' % (self.body)