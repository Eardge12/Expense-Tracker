from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from app.models import User
from app import db
import re

auth_bp = Blueprint('auth',__name__,url_prefix='/auth')

@auth_bp.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@$%&*?])[A-Za-z\d@!$%&*?]{8,}$'

    if not username or not email or not password:
        return jsonify({'message':'Missing fields'}),400
    if not re.match(email_regex,email):
        return jsonify({'message':'invalid email'}),400
    if not re.fullmatch(password_regex, password):
        return jsonify({'message':'Invalid pass*'}),400
    if User.query.filter_by(email=email).first():
        return jsonify({'message':'email already exist'}),400
    if User.query.filter_by(username=username).first():
        return jsonify({'message':'username already exist'}),400

    password_hash = generate_password_hash(password)
    new_user = User(username=username,email=email,password_hash=password_hash)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'user succesfully created'}),201


@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if not email or not password:
        return jsonify({'message':'missing fields'}),400
    if not user:
        return jsonify({'message':'User not found'}),404
    if not check_password_hash(user.password_hash, password):
        return jsonify({'message':'invalid passwrod'})
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message':'Logind succesfully ',
        'access_token': access_token
    })