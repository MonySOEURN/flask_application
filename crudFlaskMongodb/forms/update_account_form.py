from crudFlaskMongodb.forms.index import *

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min =2, max = 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_file = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        # made change by: User.objects(email=email.data).first()
        if email.data != current_user.email:
            user = User.objects().filter(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')