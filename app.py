from flask import Flask, render_template, flash, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin
from forms import ExtLoginForm
from flask_migrate import Migrate
from flask_mail import Mail
from flask_security import SQLAlchemyUserDatastore, Security, logout_user
from werkzeug.security import generate_password_hash
import os.path as op
from config import Config
from flask_ckeditor import CKEditor

# Create a Flask Instance

app = Flask(__name__)

app.config.from_object(Config)

#Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
ckeditor = CKEditor(app)

# Login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import Users, Roles, Posts
from admin import IndexView, UserModelView, MainIndexLink, PostModelView
from static_file_admin import FileAdmin

# Instantiate Flask-Admin
admin = Admin(app, index_view=IndexView(), base_template='admin/my_master.html' , template_mode='bootstrap3')

# Create Home Link
admin.add_link(MainIndexLink(name="Home"))

# Create Model Views
admin.add_view(UserModelView(Users, db.session))
admin.add_view(PostModelView(Posts, db.session))

#Create Static view
path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))


# Create a datastore and instantiate Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Users, Roles)
security = Security(app, user_datastore, login_form=ExtLoginForm)

@app.before_first_request
def create_user():
    user = Users.query.filter_by(email='admin@admin.com').first()

    if not user:
        db.drop_all()
        db.create_all()
        user_datastore.create_user(email='admin@admin.com', password='admin', name='admin')
        role = user_datastore.create_role(name='admin')
        db.session.add(role)
        user_role= user_datastore.create_role(name='user')
        db.session.add(user_role)
        user = Users.query.filter_by(email='admin@admin.com').first()
        user_datastore.add_role_to_user(user, role)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

from other import other
from auth import auth
from post_auth import post

app.register_blueprint(other)
app.register_blueprint(auth)
app.register_blueprint(post)

# app.run(host='0.0.0.0', post=4000)