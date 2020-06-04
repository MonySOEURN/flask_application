from crudFlaskMongodb.forms.index import *

from crudFlaskMongodb.models.user import User

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        # made change by: User.objects(email=email.data).first()
        user = User.objects().filter(email=email.data).first()
        if user is None:
            raise ValidationError('There is \'NO\' account with that email. You must register first.')
