from flask import Flask, g, jsonify, render_template

import config
import models
from auth import auth
from resources.todo import todos_api
from resources.user import users_api

app = Flask(__name__)
app.register_blueprint(todos_api)
app.register_blueprint(users_api)

@app.route('/')
def my_todos():
    return render_template('index.html')

@app.route('/api/v1/users/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
