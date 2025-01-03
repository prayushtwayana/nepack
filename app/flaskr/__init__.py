from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# fix hardcode imports of SECRET_KEY and SQLALCHEMY_DATABASE_URI, use .env


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # if test_config is not passed and exists in 'instance_folder', load it 
    # `config.py` is the config file
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test_config if passed in
        app.config.from_mapping(test_config)

    # make sure that the 'instance' folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app=app)

    from . import models
    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
