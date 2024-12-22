import os

class Config:
    # SQLite 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'music_player.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 允许所有来源的跨域请求
    CORS_ORIGINS = "*"