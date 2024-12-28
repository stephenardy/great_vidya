from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import *
from . import db
import string
import secrets
from sqlalchemy import select
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.DEBUG)

views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    teacher_subjects = UserSubjects.query.filter_by(user_id=current_user.id, is_teacher=True).all()
    student_subjects = UserSubjects.query.filter_by(user_id=current_user.id, is_teacher=False).all()
    return render_template('user_dashboard.html', user=current_user,teacher_subjects=teacher_subjects,student_subjects=student_subjects)

@views.route('/create-subject', methods=['GET','POST'])
@login_required
def create_subject():
    if request.method == 'POST':
        logging.debug("Received POST request for creating subject.")
        name = request.form.get('name')
        class_name = request.form.get('class_name')

        logging.debug(f"Form data: name={name}, class_name={class_name}")
        
        def generate_group_code():
            alphabet = string.ascii_letters + string.digits
            return ''.join(secrets.choice(alphabet) for i in range(7))
        
        def generate_unique_code(db, Subjects):
            logging.debug("Generating unique code for subject.")
            while True:
                code = generate_group_code()
                if not Subjects.query.filter_by(code=code).first():
                    logging.debug(f"Generated unique code: {code}")
                    return code
        try:
            code = generate_unique_code(db, Subjects)
            logging.debug(f"Unique code generated: {code}")

            new_subject = Subjects(name=name,class_name=class_name, code=code)
            db.session.add(new_subject)
            db.session.commit()
            logging.debug(f"New subject created: {new_subject.id}")

            user_subject = UserSubjects(user_id=current_user.id,subject_id=new_subject.id,is_teacher=True)
            db.session.add(user_subject)
            db.session.commit()
            logging.debug("UserSubjects association created.")

            flash('Subject successfully created!', category='success')
            logging.debug("Redirecting to home.")
            return redirect(url_for('views.home'))
        
        except Exception as e:
            logging.error(f"Error occurred during subject creation: {e}")
            db.session.rollback()
            flash(f'An error occured:{e}',category='error')

    return render_template('create_subject.html', user=current_user)

@views.route('/join-subject', methods=['GET','POST'])
@login_required
def join_subject():
    if request.method == 'POST':
        subject_code = request.form.get('code')

        subject_exist = Subjects.query.filter_by(code=subject_code).first()

        if subject_exist:
            join_subject= UserSubjects(user_id=current_user.id,subject_id=subject_exist.id,is_teacher=False)
            db.session.add(join_subject)
            db.session.commit()
            flash('Successfully join the class!', category='success')
            return redirect(url_for('views.home'))

        else:
            flash('Subject does not exists!',category='error')
        


    return render_template('join_subject.html', user=current_user)