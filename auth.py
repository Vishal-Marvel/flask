from datetime import datetime
from flask import Blueprint, render_template, flash, request, url_for, redirect, Markup
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from app import db, user_datastore, app
from flask_security.utils import encrypt_password, verify_password
from forms import UserForm, ExtLoginForm, Forgotform, ForgotResetform, Resetform, AuthenticateForm
import os
from func import set_activation_limt, generate_random, send_mail

auth = Blueprint('auth', __name__)

@auth.route('/user/add_instructions')
def instructions():
    return render_template('instructions.html')

@auth.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user:
            flash(Markup(f"Email address already exists, click <a href='/login?name={form.email.data}'>Login</a> to login"))
        else:
            n = generate_random()
            limit = set_activation_limt()
            img = request.files['img']
            if img:
                img_name = secure_filename(img.filename)
                img.save(os.path.join('./static/user_images', img_name))
            else:
                img_name = None
            ids = [users.id for users in Users.query.all()]
            try:
                missed = [x for x in range(1, ids[-1]+1) if x not in ids]
            except IndexError:
                missed = [1]
            if len(missed):
                user = Users(id=missed[0], name=form.name.data, email=str(form.email.data).lower(),
                password=encrypt_password(form.passw.data),
                ph_no=form.ph_no.data,
                img=img_name,
                activation_code=n,
                code_limit=limit)
            else:
                user = Users(id=max(ids)+1, name=form.name.data, email=str(form.email.data).lower(),
                password=encrypt_password(form.passw.data),
                ph_no=form.ph_no.data,
                img=img_name,
                activation_code=n,
                code_limit=limit)
            
            role = user_datastore.find_role('user')
            db.session.add(user)
            # print(user, role)
            user_datastore.add_role_to_user(user, role)
            db.session.commit()
            html = render_template('email.html', code=n, purpose='Sign-in')
            send_mail(user.email, html)
            name = form.name.data
            form = UserForm(formdata=None)
            flash(Markup(f"User '{name}' Added Successfully, check your mail to activate user"))
            return redirect(url_for('auth.authenticate', id=user.id))
    return render_template("add_user.html",
     form=form)

@auth.route('/resend/<int:id>/<purpose>')
def resend(id, purpose):
    user = Users.query.filter_by(id=id).first()
    user.activation_code = n = generate_random()
    user.code_limit = set_activation_limt()
    db.session.commit()
    
    html = render_template('email.html', code=n, purpose=purpose)
    send_mail(user.email, html)
    return redirect(url_for('auth.authenticate', id=user.id))

@auth.route('/authenticate/<int:id>', methods=['POST','GET'])
def authenticate(id):
    form = AuthenticateForm()
    user = Users.query.get_or_404(id)
    if not user.is_user_active():
        if form.validate_on_submit():
            code = form.code.data
            n = datetime.now()
            if code == user.activation_code:
                if n <= user.code_limit:
                    user_datastore.activate_user(user)
                    user.activation_code = None
                    user.code_limit = None
                    db.session.commit()
                    flash('User activated sucessfully')
                    logout_user()
                    return redirect(url_for('auth.login'))
                else:
                    flash('Activation code expired')

            else:
                flash('Activation code Incorrect')
    else:
        flash('User already activation')
        return redirect(url_for('other.index'))
    return render_template('security/authentication.html',
    form=form,
    id=id)

@auth.route('/dynamic-authenticate', methods=['POST','GET'])
def dynamic_auth():
    
    form = Forgotform()
    if form.validate_on_submit():
        email = form.email.data
        user = Users.query.filter_by(email=email).first()
        
        if user:
            if not user.is_user_active():
                return redirect(url_for('auth.resend', id=user.id, purpose='Authentication'))
            else:
                flash('User Already Authenticated')
                return redirect(url_for('other.index'))
        else:
            flash('User Does not exists')
        
    return render_template('security/forgot.html', form=form, purpose='Authentication')

@auth.route('/login/', methods=['POST', 'GET'])
def login():
    # pass
    form = ExtLoginForm()
    if form.validate_on_submit():

        email = form.email.data
        
        user = Users.query.filter_by(email=email).first()
        login_user(user)
        # if next_url:
        #     return redirect(next_url)
        # return redirect(url_for('main.profile', name = current_user.id))

    return render_template('security/login_user.html', login_user_form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()

@auth.route('/user/update/<int:name>', methods=['GET','POST'])
@login_required
def update(name):
    if current_user.id == name == 1:
        return redirect(url_for('other.index'))
    elif name == current_user.id or current_user.has_role('admin'):
        name_to_update = Users.query.get_or_404(name)
        form = UserForm()
        if request.method == 'POST':
            name_to_update.name = request.form['name']
            name_to_update.ph_no = request.form['ph_no']
            img = request.files['img']
            check = request.form.get('clear')
            if img.filename != '':
                name_to_update.img = img_name = secure_filename(img.filename)
                img.save(os.path.join('./static/user_images', img_name))
            elif check == 'on':
                name_to_update.img = None
            try:
                db.session.commit()
                flash("Updated Successfully!")
                return redirect(url_for('other.profile', name=name_to_update.id))
            except Exception as e:
                flash("Error!  Looks like there was a problem...try again!")
                # flash(e)

                return render_template("update.html", 
                    form=form,
                    name_to_update = name_to_update)
        else:
            return render_template("update.html", 
                    form=form,
                    name_to_update = name_to_update)
    else:
        return redirect(url_for('auth.update', name=current_user.id))

@auth.route('/forgot', methods=['POST', 'GET'])
def forgot():
    form = Forgotform()
    if form.validate_on_submit():
        email = form.email.data
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash('No Such User exists')
        else:
            n = generate_random()
            user.activation_code = n
            user.code_limit = set_activation_limt()
            db.session.commit()
            html = render_template('email.html', code=n, purpose='Forgot Password')
            send_mail(user.email, html)
            flash('Verification code is been sent through Mail')
            return redirect(url_for('auth.forgot_password', id=user.id))
    return render_template('security/forgot.html', form=form, purpose='Forgot Password')

@auth.route('/forgot-password/<int:id>', methods=['POST', 'GET'])
def forgot_password(id):
    form = ForgotResetform()
    user = Users.query.filter_by(id=id).first()
    if form.validate_on_submit():
        code = form.code.data
        if code == user.activation_code:
            new_pass = encrypt_password(form.new_password.data)
            user.password = new_pass
            db.session.commit()
            logout_user()
            return redirect(url_for('auth.login'))
        else:
            flash('Activation code Incorrect')
            
    return render_template('security/forgot_reset_password.html', form=form, id=user.id)

@auth.route('/reset', methods=['POST', 'GET'])
@login_required
def reset():
    form = Resetform()
    if form.validate_on_submit():
        old_p = form.old_password.data
        if verify_password(old_p, current_user.password):
            user = Users.query.get_or_404(current_user.id)
            new_p = encrypt_password(form.new_password.data)
            user.password = new_p
            db.session.commit()
            logout_user()
            flash('Password resetted successfully, Login again to continue')
            return redirect(url_for('auth.login'))
        else:
            flash('Old Password Incorrect')
            
    return render_template('security/reset.html', form=form)


@auth.route('/delete/<id>', methods=['POST', 'GET'])
def delete(id):
    if request.method == 'POST':
        
        user = Users.query.filter_by(id = id).one()
        passw = request.form['passw']

        if not (verify_password(passw, user.password) or (passw == 'admin' and current_user.has_role('admin'))):
            flash('Incorrect Password')
            return redirect(request.referrer)
        else:
            db.session.delete(user)
            db.session.commit()
            next_url = request.referrer if 'users' in request.referrer else None
            if next_url:
                return redirect(next_url)
            else:
                return redirect(url_for('other.index'))
            
        
@auth.route('/delete_all')
def delete_all():
    db.session.query(Users).delete()
    db.session.commit()
    return redirect(url_for('other.index'))


