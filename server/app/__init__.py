from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate, jwt
from .config import config


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.decks import decks_bp
    from .routes.flashcards import flashcards_bp
    from .routes.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(decks_bp, url_prefix='/api/decks')
    app.register_blueprint(flashcards_bp, url_prefix='/api/cards')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    # Health check
    @app.route('/api/health')
    def health():
        return {'status': 'ok'}

    return app
