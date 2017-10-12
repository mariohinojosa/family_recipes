from flask_wtf import FlaskForm as Form
from wtforms import StringField
from wtforms.validators import DataRequired


class AddRecipeForm(Form):
    """docstring for AddRecipeForm"""
    recipe_title = StringField('Recipe Title', validators=[DataRequired()])
    recipe_description = StringField('Recipe Description', validators=[DataRequired()])
