import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db' # 推荐使用相对instance的路径
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev' # 只在开发环境使用'dev'，生产环境必须设置环境变量
    CORS_ORIGINS = "*"
    CORS_HEADERS = "Content-Type"