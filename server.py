from recipes_flask_app import app
from recipes_flask_app.controllers import users
from recipes_flask_app.controllers import recipes


if __name__ == '__main__':
    app.run(debug=True)