from app import create_app
from config import Config
from flask_cors import CORS

app = create_app()
app.config.from_object(Config)

# 初始化 Flask-CORS
CORS(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=21600)