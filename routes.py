from flask import Flask, render_template, request, redirect, url_for
from .forms import MealForm
from .utils import process_meal

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MealForm()
    if form.validate_on_submit():
        meal_type = form.meal_type.data
        year = form.year.data
        month = form.month.data
        day = form.day.data
        calorie_goal = form.calorie_goal.data
        protein_goal = form.protein_goal.data
        dietary_restrictions = form.dietary_restrictions.data
        dining_hall = form.dining_hall.data

        # Process the meal and get recommendations
        recommendations = process_meal(meal_type, year, month, day, calorie_goal, protein_goal, dining_hall, dietary_restrictions)

        return render_template('index.html', form=form, recommendations=recommendations)

    return render_template('index.html', form=form)