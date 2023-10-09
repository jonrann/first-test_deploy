from recipes_flask_app import app
from recipes_flask_app.models import user as user_module

from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask import render_template, redirect, request, session, url_for, flash

bcrpt = Bcrypt(app)

@app.route('/')
def login_register():
    if 'user_id' in session:
        return redirect(url_for('recipe_dashboard'))
    return render_template('login_register.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirmPassword']
    
    data = {
        'first_name' : first_name,
        'last_name' : last_name,
        'email' : email,
        'password' : password,
        'confirm_password' : confirm_password
    }

    if not user_module.Users.validate_user_data(data):
        return redirect(url_for('login_register'))
    
    hashed_password = generate_password_hash(data['password'])
    data['password'] = hashed_password

    if user_module.Users.create(data):
        flash('Register successful!', 'register_success')
        return redirect(url_for('login_register'))
    

@app.route('/login', methods=['POST'])
def login():
    login_email = request.form['loginEmail']
    login_password = request.form['loginPassword']

    user = user_module.Users.get_one_by_email(login_email)
    if user:
        print(check_password_hash(user.password, login_password))
        if check_password_hash(user.password, login_password):
            session['user_id'] = user.id
            flash('Login successful!', 'login_success')
            return redirect(url_for('recipe_dashboard'))
        else:
            flash('Incorrect password, try again', 'login_error')
            return redirect(url_for('login_register'))

    else:
        flash('Email not found, try again', 'login_error')
        return(redirect(url_for('login_register')))

@app.route('/recipes')
def recipe_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
    print(user_id)
    current_user = user_module.Users.get_one_by_id(user_id)
    recipes_list = user_module.Users.get_users_with_recipes()
    return render_template('recipe_dashboard.html', current_user=current_user, recipes_list=recipes_list)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login_register'))
