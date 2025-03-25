from flask import render_template, flash, redirect, url_for, session
from app.forms import LoginForm
from app.models import People
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_routes(app):
    @app.route('/')
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'user_id' in session:
            return redirect(url_for('index'))
            
        form = LoginForm()
        if form.validate_on_submit():
            person = People.query.filter_by(
                PeopleID=form.people_id.data,
                Phone=form.phone.data
            ).first()
            
            if person:
                session['user_id'] = person.PeopleID
                flash(f'Login successful for {person.FirstName}', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid People ID or phone number', 'danger')
        return render_template('login.html', title='Sign In', form=form)

    @app.route('/index')
    @login_required
    def index():
        return render_template('index.html', title='Home')

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))