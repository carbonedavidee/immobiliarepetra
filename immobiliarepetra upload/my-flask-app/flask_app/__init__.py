from flask import Flask , session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__,static_folder='../../my-vue-app/dist', static_url_path='')
app.secret_key = "owjhfwoifjwfijwfowejfweoif898932u392"
app.permanent_session_lifetime = timedelta(days=3)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'immobiliarepetraa@gmail.com'  
app.config['MAIL_PASSWORD'] = 'uypomvemxfxyfnta'     
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
app.app_context().push()


from flask_app import public_routes
from flask_app import admin_routes
from flask_app import api_routes
from flask_app import flash_manager
from flask_app import mail_manager




