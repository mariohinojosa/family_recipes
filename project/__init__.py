from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

from project.users.views import users_blueprint
from project.recipes.views import recipes_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(recipes_blueprint)
