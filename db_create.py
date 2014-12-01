# db_create.py


from views import db
from models import User
from datetime import date

# create the database and the db table
db.create_all()

# insert data
db.session.add(User("testuser1", "admin@alpha-legion.pro", "password"))
# db.session.add(Task("Finish Real Python", date(2014, 3, 13), 10, 1))

# commit the changes
db.session.commit()