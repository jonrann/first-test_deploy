from flask import Flask

app = Flask(__name__)
app.secret_key = 'this_the_key_to_food'