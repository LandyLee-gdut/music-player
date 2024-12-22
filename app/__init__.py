import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 导入 CORS
from app.models.db import db
from app.routes.RecentlyPlayedRoutes import recently_played_bp

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',  # 建议在配置中设置
        DATABASE=os.path.join(app.instance_path, 'music_player.db')
    )
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///' + app.config['DATABASE'])
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

    # 确保 instance 文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(recently_played_bp)

    with app.app_context():
        db.create_all()

    return app