import os
import uuid


from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt import JWT, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from EmailSending import sending_email

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "MYSECRETKEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['DATABASE_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

########################################################################################################3
class User(db.Model):
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key = True)
    token_id = db.Column(db.String(100), unique = True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    password = db.Column(db.String(100))
    email_addr = db.Column(db.Text, unique = True)

#############################################################################################################
@app.route('/user', methods = ['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    token_id = uuid.uuid4()
    
    user = User(
        token_id = str(token_id),
        first_name = data['first_name'],
        last_name = data['last_name'],
        password = hashed_password,
        email_addr = data['email_addr']
    )
    # receiver = user.email_addr
    token_id = user.token_id

    # sending_email(receiver = receiver, subject = 'Token_number', token_id = token_id)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'The user has been added'})

@app.route('/login', methods = ['POST', 'GET'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email_addr = data['email_addr']).first()

    if user and check_password_hash(user.password, data['password']):
        return jsonify({
            'Informations': {
                'ID': user.id, 
                'first_name': user.first_name, 
                'last_name': user.last_name
            }
        })


@app.route('/write/<string:token_id>', methods = ['POST'])
def write_profile(token_id):
    user = User.query.filter_by(token_id = token_id).first()

    if not user:
        return jsonify({'message': 'Try to Enter the exact token_id'})

    else:
        data = request.get_json()
        user.last_name = data['last_name']
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'ID': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email_addr': user.email_addr, 
            'password': user.password
        })


if __name__ == '__main__':
    app.run(debug = True)