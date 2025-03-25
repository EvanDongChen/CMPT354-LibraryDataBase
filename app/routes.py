from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from app.models import People

def init_routes(app):
    @app.route('/')
    @app.route('/base')
    @app.route('/index')
    def index():
        return render_template('index.html', title='Home')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            person = People.query.filter_by(
                PeopleID=form.people_id.data,
                Phone=form.phone.data
            ).first()
            
            if person:
                flash(f'Login successful for {person.FirstName}', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid People ID or phone number', 'danger')
        return render_template('login.html', title='Sign In', form=form)