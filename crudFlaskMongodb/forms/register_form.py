from crudFlaskMongodb.forms.index import *

from crudFlaskMongodb.models.user import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min =2, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        # made change by: User.objects(email=email.data).first()
        user = User.objects().filter(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')