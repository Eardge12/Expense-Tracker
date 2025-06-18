from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS



db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secret'
    
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from .routes.auth import auth_bp
    from .routes.expenses import expenses_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)

    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"Endpoint:{rule.endpoint},Rule:{rule}")
    return app
    

