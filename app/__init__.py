from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

from app import routes

if __name__ == "__init__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
