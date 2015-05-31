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
	stata_id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __repr__(self):
		return '<Post %r>' % (self.body)