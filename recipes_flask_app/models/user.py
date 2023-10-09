from recipes_flask_app.config.mysqlconnection import connectToMySQL
from recipes_flask_app.models import recipe as recipe_module
from flask import flash

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Users:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']  # It's better to handle passwords securely, not as plain text
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (
                first_name, 
                last_name, 
                email, 
                password, 
                created_at, 
                updated_at
            ) 
                VALUES (
                %(first_name)s, 
                %(last_name)s, 
                %(email)s, 
                %(password)s,
                NOW(), 
                NOW()
            );
        """
        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('recipes').query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_one_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {
            'id' : user_id
        }
        result = connectToMySQL('recipes').query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None

    #Get by email
    @classmethod
    def get_one_by_email(cls, user_email):
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = {
            'email' : user_email
        }
        result = connectToMySQL('recipes').query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None
        
    @classmethod
    def get_users_with_recipes(cls):
        query = """
            SELECT * FROM recipes
            JOIN users ON recipes.user_id = users.id
            ORDER BY recipes.updated_at DESC;
        """
        # Execute the query
        results = connectToMySQL('recipes').query_db(query)
        
        # List to hold recipe objects
        recipes_list = []

        for row in results:
            # Create a User object
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user = cls(user_data)
            
            # Create a Recipe object
            recipe_data = {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'instructions': row['instructions'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'under': row['under'],
                'user_id': row['user_id']
            }
            recipe = recipe_module.Recipes(recipe_data)
            # Associate the User object with the Recipe object
            recipe.creator = user
            print(recipe.creator)
            # Add the Recipe object to the recipes list
            recipes_list.append(recipe)
        
        return recipes_list


    
    # Validate User information
    @staticmethod
    def validate_user_data(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name needs to be at least 2 characters', 'register_error')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name needs to be at least 2 characters', 'register_error')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email', 'register_error')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password needs to be at least 8 characters', 'register_error')

        #Password
        if not re.search("[A-Z]", data['password']):
            flash('Password needs at least one uppercase letter', 'register_error')
            is_valid = False
        if not re.search("[0-9]", data['password']):
            flash('Password needs at least one number', 'register_error')
            is_valid = False

        #Validate password match
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match', 'register_error')
            is_valid = False
        return is_valid
