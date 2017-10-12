import os
import unittest
from project import app, db

TEST_DB = 'user.db'


class UserTests(unittest.TestCase):
    """This class will include functions to setUp() and tearDown() each unit test.
    The setUp() function should specify the key configuration items
    needed for the unit test case.
    The tearDown() function will not
    do anything to start off"""
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    # Helper function
    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
            )

    # check that login page renders properly
    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertIn(b'Future site for logging into Mario\'s Family Recipes!',
                      response.data)

    # check that the registration page comes up correctly,
    # as indicated by getting a ‘200’ code back when we request the page:
    def test_user_registration_form_displays(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please Register Your New Account', response.data)

    # check that a valid user registration entry works:
    def test_valid_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@gmail.com', 'FlaskIsAwesome',
                                 'FlaskIsAwesome')
        self.assertIn(b'Thanks for registering!', response.data)

    # check that entering a duplicate email causes an error to occur:
    def test_duplicate_email_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@yahoo.com', 'FlaskIsAwesome',
                      'FlaskIsAwesome')
        self.app.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@yahoo.com',
                                 'FlaskIsReallyAwesome',
                                 'FlaskIsReallyAwesome')
        self.assertIn(b'ERROR! Email (patkennedy79@yahoo.com) already exists.',
                      response.data)

    # check that an incomplete form causes an error:
    def test_missing_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response = self.register('patkennedy79@gmail.com', 'FlaskIsAwesome',
                                 '')
        self.assertIn(b'This field is required.', response.data)


if __name__ == '__main__':
    unittest.main()
