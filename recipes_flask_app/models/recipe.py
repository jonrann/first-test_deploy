from recipes_flask_app.config.mysqlconnection import connectToMySQL
from recipes_flask_app.models import user as user_module
from flask import flash

class Recipes:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.under = data['under']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO recipes (
                name,
                description,
                instructions,
                created_at,
                under,
                user_id
            )
            VALUES (
                %(name)s,
                %(description)s,
                %(instructions)s,
                %(created_at)s,
                %(under)s,
                %(user_id)s
            )
        """
        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def get_by_id(cls, recipe_id):
        query = """
            SELECT recipes.*, users.*
            FROM recipes
            JOIN users ON recipes.user_id = users.id
            WHERE recipes.id = %(recipe_id)s;
        """
        data = {
            'recipe_id': recipe_id
        }
        results = connectToMySQL('recipes').query_db(query, data)
        if results:
            row = results[0]
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
            recipe = cls(recipe_data)  # Creating a Recipes object
            
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            recipe.creator = user_module.Users(user_data)  # Setting the creator attribute with a Users object
        
            return recipe  # Returning the Recipes object with the creator attribute set
        return None  # Returning None if no results are found


    @classmethod
    def update(cls, data):
        query = """
            UPDATE recipes
            SET name = %(name)s,
                description = %(description)s,
                instructions = %(instructions)s,
                updated_at = NOW(),
                under = %(under)s
            WHERE id = %(id)s;
        """
        return connectToMySQL('recipes').query_db(query, data)
    

    @classmethod
    def delete(cls, recipe_id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {
            'id': recipe_id
        }
        result = connectToMySQL('recipes').query_db(query, data)
        return True if result else False

    
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Name needs to be at least 3 characters', 'register_error')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description must be at least 3 characters', 'register_error')
            is_valid = False
        if len(data['instructions']) < 3:
            flash('Instructions must be at least 3 characters', 'register_error')
            is_valid = False
        return is_valid
