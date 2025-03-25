from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from backend.app.models import People

class LoginForm(FlaskForm):
    people_id = StringField('People ID', validators=[DataRequired(), Length(min=1, max=10)])
    phone = PasswordField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_people_id(self, people_id):
        person = People.query.filter_by(PeopleID=people_id.data).first()
        if person is None:
            raise ValidationError('Invalid People ID')

    def validate_phone(self, phone):
        person = People.query.filter_by(Phone=phone.data).first()
        if person is None:
            raise ValidationError('Invalid phone number')
        # Verify the phone matches the people_id
        if hasattr(self, 'people_id') and self.people_id.data:
            correct_person = People.query.filter_by(
                PeopleID=self.people_id.data,
                Phone=phone.data
            ).first()
            if not correct_person:
                raise ValidationError('Phone number does not match People ID')