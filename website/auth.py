from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import db
from .models import *
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        user_name = User.query.filter_by(username=username).first()

        if user:
            flash('Email already exists.', category='error')
        elif user_name:
            flash('Username already exists. Try another username.', category='error')
        elif len(username) < 3:
            flash('Username must be greater than 2 charachters!', category='error')
        elif password1 != password2:
            flash('Password did not match!', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters long', category='error')
        else:
            new_user = User(email=email,username=username,password=generate_password_hash(password1,method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash('Acccount created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))


    return render_template('sign_up.html', user=current_user)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
        user = User.query.filter_by(username=username).first()
        
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Please try again!', category='error')
        else:
            flash('Username does not exists.', category='error')
    
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))