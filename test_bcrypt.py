# test.py

import os
import unittest

from views import app, db, bcrypt
from config import basedir
from models import User
    
TEST_DB = 'test.db'

class AllTests(unittest.TestCase):
    #############################################################################################################################################
    #                                                           HELPER METHODS                                                                  #
    def register(self, name, email, password, confirm):
        return self.app.post('register/', data = dict(name = name, email = email, password = password, confirm = confirm), follow_redirects = True)

    def login(self, name, password):
        return self.app.post('/', data = dict(name = name, password = password), follow_redirects = True)




    def create_user(self):
        new_user = User(
        name='dnar',
        email='dnar@dno.ru',
        password=bcrypt.generate_password_hash('1234')
        )
        db.session.add(new_user)
        db.session.commit()
    #                                                                                                                                           #
    #############################################################################################################################################


    #setup and teardown
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB) 
        
        self.app = app.test_client()
        db.create_all()

    # login test
    def test_user_can_login(self):
        self.register('dnishe', 'dnishe@aol.com', '1234', '1234')
        response = self.login('dnishe', '1234')
        self.assertIn('Successfully logged in', response.data)

    def tearDown(self):
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
