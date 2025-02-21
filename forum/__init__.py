from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import declarative_base
from flask_login import LoginManager
from forum.database import db, Base
from forum.create_database import init_db

app = Flask(__name__, static_folder="static")

try:
    Base.query = db.session.query_property()
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "..", "cmt120_cw2.db")
        
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Set redirect page when not logged in
    login_manager.login_view = "home" 
    init_db(app, db)
except Exception as e:
    print(f"Exception caught: {e}")

# Import route
import forum.router
