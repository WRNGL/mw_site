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

	def __init__(self, name = None, email = None, password = None):
		self.name = name
		self.email = email
		self.password = password

	def __repr__(self):
		return '<User %r>' % (self.name)

class Stata(db.Model):
	__tablename__ = 'stata'
	stata_id = db.Column(db.Integer, primary_key = True)
	mc = db.Column(db.String(8))
	kills = db.Column(db.String(8))
	deaths = db.Column(db.String(8))
	cbills = db.Column(db.String(10))
	exp_points = db.Column(db.String(20))
	wins = db.Column(db.String(8))
	losses = db.Column(db.String(8))
	timestamp = db.Column(db.Date, default=datetime.datetime.utcnow())
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