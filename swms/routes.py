import secrets
import os
from PIL import Image
import sys
import serial, time

from swms import app, db, bcrypt, mail
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, CreateDustbinForm
from swms.models import User, Dustbin


@app.route('/')
@app.route('/dashboard')
@login_required
def home():
    total_count = User.query.count()
    admin_count = User.query.filter_by(role='admin').count()
    user_count = User.query.filter_by(role='user').count()
    dustbin_count = Dustbin.query.count()
    return render_template('animated-dashboard.html', title="Dashboard", total_count=total_count, user_count=user_count,
                           admin_count=admin_count, dustbin_count=dustbin_count)


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
    dustbins = Dustbin.query.all()
    return render_template('dustbin-list.html', dustbins=dustbins)


@app.route('/dustbin', methods=['GET', 'POST'])
@login_required
def create_dusbtbin():
    if current_user.role == 'admin':
        form = CreateDustbinForm()
        form.users_id.choices = [(users_id.id, users_id.fullname) for users_id in
                                 User.query.filter_by(role="user").all()]

        if form.validate_on_submit():
            print(form.dustbinName.data)
            dustbin = Dustbin(dustbin_name=form.dustbinName.data, description=form.description.data,
                              location=form.location.data,
                              users_id=form.users_id.data)
            db.session.add(dustbin)
            db.session.commit()
            flash(f'Dustbin created for {form.dustbinName.data}!', 'success')
            return redirect(url_for('home'))

        return render_template('create-dustbin.html', title='Create Dustbin', form=form)


# /dev/ttyACM0

@app.route('/dustbinStatus/<int:id>', methods=['GET'])
@login_required
def dustbin_status(id):
    """Opening of the serial port"""
    try:
        arduino = serial.Serial("COM6", 9600, timeout=1)
        time.sleep(5)

    except:
        print('Please check the port')

    """Initialising variables"""
    rawdata = []
    count = 0

    """Receiving data and storing it in a list"""
    while count < 1:
        rawdata.append(str(arduino.readline(), 'utf-8'))
        count += 1

    rawstring = ''.join(rawdata).replace('\n', '').replace('\r', '')
    splitstring = rawstring.split(",")
    ultrasonic = splitstring[:1]
    gas = splitstring[1:]

    if ultrasonic == ['100'] or gas == ['1']:
        dustbin = Dustbin.query.filter_by(users_id=id).first()
        user = User.query.filter_by(id=dustbin.users_id).first()
        msg = Message('Smart Waste Management', sender='intensenotes@gmail.com', recipients=[user.email])
        msg.body = "Hello, Please remove the wastes in the waste-bin. "
        mail.send(msg)
        flash(f'Message sent!', 'success')

    return render_template('sensor-status.html', ultrasonic=ultrasonic, gas=gas)


@app.route('/sendEmail/<int:id>', methods=['GET'])
@login_required
def send_email(id):
    dustbin = Dustbin.query.filter_by(users_id=id).first()
    user = User.query.filter_by(id=dustbin.users_id).first()
    msg = Message('Smart Waste Management', sender='intensenotes@gmail.com', recipients=[user.email])
    msg.body = "Hello, Please remove the wastes in the waste-bin. "
    mail.send(msg)
    flash(f'Message sent!', 'success')
    return redirect(url_for('dustbin_list'))


@app.route("/test", methods=['GET'])
@login_required
def test():
    rough = ['1\r\n', '0\r\n']
    ultrasonic = rough[:1]
    gas = rough[1:]

    return render_template('dustbin-list.html', ultrasonic=ultrasonic, gas=gas)
