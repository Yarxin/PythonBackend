from flask import Flask
from flask import request
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
import sqlite3
from sqlite3 import Error
from werkzeug.security import safe_str_cmp
import os
import PageBackNeural

dirname = os.path.dirname(__file__)
db = os.path.join(dirname, 'FlaskLogin.db')

__network = 0


def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as ex:
        print(ex)
    finally:
        if conn:
            conn.close()


create_connection(db)

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FlaskLogin.db'
app.config['SECRET_KEY'] = 'bardzo_tajny_klucz'
db = SQLAlchemy(app)
CORS(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)


def authenticate(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()


def process_image_internal(image):
    network_output = False
    try:
        network_output = PageBackNeural.main(image)
    except:
        print('Processing error')
    return network_output


jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return "{ value: true }"


@app.route('/process', methods=['POST'])
def process_image():
    image = request.files['image']
    network_output = process_image_internal(image)

    return "{ value: " + str(network_output) + " }"


if __name__ == '__main__':
    app.run()