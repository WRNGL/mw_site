# db_create.py


from views import db
#from models import User, Stata
#from datetime import date

# create the database and the db table
db.create_all()

# commit the changes
db.session.commit()