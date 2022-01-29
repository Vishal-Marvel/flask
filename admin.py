from flask_admin import Admin, BaseView, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, login_required
from flask import *
import time

class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            flash("Please Login to access this page")
            return redirect(url_for('auth.login', next=request.url))
        else:
            flash("You Don't Have access there!")
            return redirect(url_for('other.index'))

class IndexView(AdminMixin, AdminIndexView):
    def is_visible(self):
        return False

class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for("other.index")

class UserModelView(AdminMixin, ModelView):

    column_list = ['id', 'name', 'email', 'active']
    column_searchable_list = ['name']
    create_modal = False

class PostModelView(ModelView, AdminMixin):
    column_list = ['id', 'title', 'poster_id']
    create_model = False
