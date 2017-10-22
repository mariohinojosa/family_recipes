from project import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property


class Recipe(db.Model):
    """docstring for Recipe"""
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    recipe_title = db.Column(db.String, nullable=False)
    recipe_description = db.Column(db.String, nullable=False)

    def __init__(self, title, description):
        self.recipe_title = title
        self.recipe_description = description

    def __repr__(self):
        return 'title {}'.format(self.name)


class User(db.Model):
    """docstring for User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email, password_plaintext):
        self.email = email
        self.password = password_plaintext
        self.authenticated = False

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, password_plaintext):
        self._password = bcrypt.generate_password_hash(password_plaintext)

    @hybrid_method
    def is_correct_password(self, password_plaintext):
        return bcrypt.check_password_hash(self.password, password_plaintext)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def __repr__(self):
        return '<User {0}>'.format(self.name)
