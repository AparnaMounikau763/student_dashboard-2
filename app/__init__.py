from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # ✅ IMPORTANT: use in-memory DB for testing
    if app.config.get("TESTING"):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # ✅ FIX: NO prefix (this fixes ALL 404 errors)
    from .routes import main
    app.register_blueprint(main)

    # Health check
    @app.route('/health')
    def health():
        return jsonify({"status": "ok"})

    return app