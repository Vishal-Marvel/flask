from flask import *
from models import Users, roles_users_table
from sqlalchemy import func, Date, cast
from datetime import datetime, date
from flask_security import current_user
from forms import *

other = Blueprint('other', __name__)

@other.route('/')
def index():
    return render_template("index.html")

@other.route('/user/profile/<name>')
def profile(name):
    user = Users.query.get_or_404(name)
    form = UserForm()
    return render_template('profile.html', user=user, form=form)

@other.route('/users', methods=['POST', 'GET'])
def users():
    form = SearchForm()
    full_users = list(Users.query.all())[1:]
    if request.method == 'POST':
        searched = form.search.data
        search_by = form.select.data
        if search_by == 'User Name':
            users = list(Users.query.filter(Users.name.like('%' + searched + '%')))
        elif search_by == 'Email Id':
            users = list(Users.query.filter(Users.email.like('%' + searched + '%')))
        for index, i in enumerate(users):
            if i.id == 1:
                del users[index]
        if len(users):
            users == None
        # resulS
        return render_template('search.html',
        form=form,
        our_users=full_users,
        searched=searched,
        users=users)

    return render_template('search.html',form=form, our_users=full_users)
