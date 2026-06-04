import os
from flask import Flask, render_template
from .database import init_db
from .routes import tasks_bp


def create_app():
    app = Flask(__name__)
    app.config['ENV'] = os.getenv('APP_ENV', 'development')
    app.config['DEBUG'] = os.getenv('DEBUG', 'true').lower() == 'true'

    init_db()
    app.register_blueprint(tasks_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
