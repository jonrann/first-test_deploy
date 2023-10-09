from recipes_flask_app import app
from recipes_flask_app.models import recipe as recipe_module
from recipes_flask_app.models import user as user_module
from flask import render_template, redirect, request, session, url_for, flash

@app.route('/recipes/new')
def create_recipe_page():
    return render_template('create_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    name = request.form['name']
    description = request.form['description']
    instructions = request.form['instructions']
    created_at = request.form['date']
    under = request.form['under30']
    user_id = session['user_id']

    data = {
        'name' : name,
        'description' : description,
        'instructions' : instructions,
        'created_at' :created_at,
        'under' : under,
        'user_id' : user_id
    }
    if not recipe_module.Recipes.validate_recipe(data):
        return redirect(url_for('create_recipe_page'))
    
    if recipe_module.Recipes.create(data):
        flash('Recipe successfully created!', 'success') #Might need to fix this later to match HTML
        return redirect(url_for('recipe_dashboard'))
    
@app.route('/recipes/<int:recipe_id>')
def recipe_page(recipe_id):
    recipe = recipe_module.Recipes.get_by_id(recipe_id)
    print(recipe)
    if 'user_id' in session:
        user_id = session['user_id']
    users = user_module.Users.get_all()
    current_user = user_module.Users.get_one_by_id(user_id)

    return render_template('recipe_details.html', users=users, recipe=recipe, current_user=current_user)

from flask import session, redirect, url_for, flash

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe_page(recipe_id):
    recipe = recipe_module.Recipes.get_by_id(recipe_id)
    current_user_id = session['user_id']

    if recipe is None:
        flash('The requested recipe does not exist.', 'error')
        return redirect(url_for('recipe_dashboard'))

    if current_user_id != recipe.user_id:
        flash('You do not have permission to edit this recipe.', 'error')
        return redirect(url_for('recipe_dashboard'))
    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/recipes/update/<int:recipe_id>', methods=['POST'])
def update(recipe_id):
    recipe = recipe_module.Recipes.get_by_id(recipe_id)
    data_form = request.form
    data = {
        'id' : recipe.id,
        'name' : data_form['name'],
        'description' : data_form['description'],
        'instructions' : data_form['instructions'],
        'created_at' : data_form['date'],
        'under' : data_form['under30'],
    }
    if not recipe_module.Recipes.validate_recipe(data):
        return redirect(url_for('create_recipe_page'))
    else:
        recipe_module.Recipes.update(data)
        flash('Succesfully updated recipe!', 'success')
        return redirect(url_for('recipe_page', recipe_id=recipe_id))

@app.route('/recipes/delete/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    if recipe_module.Recipes.delete(recipe_id) != None:
        flash('Recipe deleted successfully!', 'success')
    else:
        flash('There was an error deleting the recipe', 'error')
    return redirect(url_for('recipe_dashboard'))



