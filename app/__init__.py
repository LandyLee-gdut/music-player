import os
from flask import Flask
from flask_cors import CORS
from app.models.db import db
from app.routes.RecentlyPlayedRoute import recently_played_bp
from app.routes.SongItemListRoute import song_list_bp
from config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database: {e}")
            raise

    app.register_blueprint(recently_played_bp)
    app.register_blueprint(song_list_bp)

    return app