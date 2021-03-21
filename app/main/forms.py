from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
    SubmitField, DateTimeField, DateField, IntegerField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp

from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MassDiffForm(FlaskForm):
    initial_date = DateField('Pick a Date of birth', format="%m/%d/%Y", validators=[DataRequired()])
    initial_weight = IntegerField('Initial, Kilos', validators=[DataRequired()])
    actual_date = DateField('Last Measure date', format="%m/%d/%Y", validators=[DataRequired()])
    actual_weight = IntegerField('Actual Kilos', validators=[DataRequired()])
    submit = SubmitField('Check Weight')


# Ile mleka dla noworodka karmionego butelką? Oblicz wielkość porcji!
# Eksperci ds. żywienia dzieci stworzyli wzór, dzięki któremu obliczysz idealną wielkość porcji mleka,
# z uwzględnieniem wieku dziecka. W pierwszych 10. dniach życia maluszka możemy obliczyć to następująco:
# Wielkość porcji w mililitrach = 10 x (dzień życia – 1)
# Potem (po 10. dniu życia) karmienie noworodka i obliczenie prawidłowej wielkości porcji ułatwi następujący wzór:
# Wielkość porcji w mililitrach = 100 + (miesiąc życia x 10)
# Znajomość wzoru z pewnością daje orientacyjną odpowiedź na pytanie,
# ile mleka pije noworodek. Znacznie prościej i wygodniej będzie Ci jednak po prostu
# trzymać się zaleceń umieszczonych na opakowaniu mleka modyfikowanego.

class MilkInfantForm(FlaskForm):
    actual_days = IntegerField('Age day', validators=[DataRequired()])
    submit = SubmitField('Check Milk')
