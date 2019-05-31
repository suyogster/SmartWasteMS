import secrets
import os
from PIL import Image
import sys

from swms import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, CreateDustbinForm
from swms.models import User,Dustbin


@app.route('/')
@app.route('/dashboard')
@login_required
def home():
    total_count = User.query.count()
    admin_count = User.query.filter_by(role='admin').count()
    user_count = User.query.filter_by(role='user').count()
    return render_template('animated-dashboard.html', title="Dashboard", total_count=total_count, user_count=user_count,
                           admin_count=admin_count)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role == 'admin':
        form = RegistrationForm()
        print(current_user.fullname, file=sys.stdout)
        if form.validate_on_submit():
            form.created_by.data = current_user.fullname
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(fullname=form.fullname.data, email=form.email.data, password=hashed_password,
                        role=form.role.data, created_by=form.created_by.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.fullname.data}!', 'success')
            return redirect(url_for('home'))
        return render_template('page-register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You are successfully logged in as {current_user.fullname}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'LogIn Unsuccessful!', 'danger')
    return render_template('page-login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash(f'Logout Successful', 'success')
    return redirect('login')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/avatar', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.fullname = form.fullname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='images/avatar/' + current_user.image_file)
    return render_template('account.html', title='Account', image=image_file, form=form)


@app.route('/usersList')
@login_required
def user_list():
    users = User.query.filter_by(role='user').all()
    return render_template('user-list.html', title='User List', users=users)


@app.route('/editUser/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.role == 'admin':
        user = User.query.filter_by(id=id).first()
        form = UpdateAccountForm()
        if form.validate_on_submit():
            user.fullname = form.fullname.data
            user.email = form.email.data
            db.session.commit()
            flash('Your Account has been updated', 'success')
            return redirect(url_for('user_list'))
        return render_template('edit-user.html', title='Edit User', user=user, form=form)
    else:
        flash('You have no right no access the page', 'danger')
        return redirect(url_for('login'))


@app.route('/deleteUser/<int:id>', methods=['GET'])
@login_required
def delete_user(id):
    if current_user.role == 'admin':
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        flash('The Account has been deleted', 'success')
        return redirect(url_for('user_list'))
    else:
        flash('You have no right no access the page', 'danger')
        return redirect(url_for('login'))


@app.route('/dustbinList')
@login_required
def dustbin_list():
    return render_template('dustbin-list.html')


@app.route('/dustbin', methods=['GET', 'POST'])
@login_required
def create_dusbtbin():
    user_list = db.session.query()
    if current_user.role == 'admin':
        form = CreateDustbinForm()

        if form.validate_on_submit():
            return "hello"
