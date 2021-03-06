import os
import unittest
from project import app, db, mail

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

        mail.init_app(app)
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

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
            )

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

    def test_login_form_displays(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)

    def test_valid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'patkennedy79@gmail.com', response.data)

    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response = self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        self.assertIn(b'ERROR! Incorrect login credentials.', response.data)

    def test_valid_logout(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Goodbye!', response.data)

    def test_invalid_logout_within_being_logged_in(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Log In', response.data)

    def test_user_profile_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        response = self.app.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Address', response.data)
        self.assertIn(b'Account Actions', response.data)
        self.assertIn(b'Statistics', response.data)
        self.assertIn(b'First time logged in. Welcome!', response.data)

    def test_user_profile_page_after_logging_in(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.get('/logout', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')
        response = self.app.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Address', response.data)
        self.assertIn(b'Account Actions', response.data)
        self.assertIn(b'Statistics', response.data)
        self.assertIn(b'Last Logged In: ', response.data)

    def test_user_profile_without_logging_in(self):
        response = self.app.get('/user_profile')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Fuser_profile', response.data)

    def test_change_email_address_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        response = self.app.get('/email_change')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Current Email: patkennedy79@gmail.com', response.data)
        self.assertIn(b'Please enter your new email address:', response.data)

    def test_change_email_address(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.app.post('/email_change', data=dict(email='patkennedy79@blaa.com'), follow_redirects=True)
        response = self.app.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email Address', response.data)
        self.assertIn(b'patkennedy79@blaa.com', response.data)
        self.assertNotIn(b'patkennedy79@gmail.com', response.data)

    def test_change_email_address_with_existing_email(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        response = self.app.post('/email_change', data=dict(email='patkennedy79@gmail.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sorry, that email already exists!', response.data)
        self.assertIn(b'Current Email: patkennedy79@gmail.com', response.data)
        self.assertIn(b'Please enter your new email address:', response.data)

    def test_change_email_without_logging_in(self):
        response = self.app.get('/email_change')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Femail_change', response.data)
        response = self.app.post('/email_change', data=dict(email='patkennedy79@gmail.com'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        self.assertIn(b'Need an account?', response.data)

    def test_change_password_page(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        response = self.app.get('/password_change')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password Change', response.data)

    def test_change_password(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        response = self.app.post('/password_change', data=dict(password='MyNewPassword1234'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password has been updated!', response.data)
        self.assertIn(b'User Profile', response.data)

    def test_change_password_logging_in(self):
        response = self.app.get('/password_change')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to target URL:', response.data)
        self.assertIn(b'/login?next=%2Fpassword_change', response.data)
        response = self.app.post('/password_change', data=dict(password='MyNewPassword1234'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
        self.assertIn(b'Need an account?', response.data)


if __name__ == '__main__':
    unittest.main()
