# db_migrate.py

from views import db
from datetime import datetime
from config import DATABASE_PATH
import sqlite3

with sqlite3.connect(DATABASE_PATH) as connection:
	# get a crusor object to execute SQL commands
	c = connection.cursor()

	# temporarily change the name of stata table
	c.execute(""" ALTER TABLE stata RENAME TO old_stata""")

	# recreate new table 
	db.create_all()

	# retrieve data from old table
	c.execute(""" SELECT body, timestamp, user_id FROM old_stata  ORDER BY stata_id ASC """)

	# save all rows as a list of tuples; set date to nowand user id to 1
	data = #TBD