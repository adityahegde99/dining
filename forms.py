from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class MealForm(FlaskForm):
    month = StringField('Month (mm)', validators=[DataRequired()])
    day = StringField('Day (dd)', validators=[DataRequired()])
    year = StringField('Year (yyyy)', validators=[DataRequired()])
    calorie_goal = IntegerField('Daily Calorie Goal', validators=[DataRequired(), NumberRange(min=1)])
    protein_goal = IntegerField('Daily Protein Goal (g)', validators=[DataRequired(), NumberRange(min=1)])
    dietary_restrictions = StringField('Dietary Restrictions (e.g., vegetarian, no nuts, gluten-free)', validators=[Optional()])
    dining_hall = SelectField('Dining Hall', choices=[('north-ave-dining-hall', 'North Avenue'), ('west-village', 'West Village')], validators=[DataRequired()])
    submit = SubmitField('Get Meal Recommendations')