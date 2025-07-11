from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import vehi_log_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'vehi_log.vehi_log_login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(vehi_log_bp, url_prefix='/vehi_log')
    
    # Root route redirect
    @app.route('/')
    def root():
        return redirect(url_for('vehi_log.vehi_log_index'))
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)