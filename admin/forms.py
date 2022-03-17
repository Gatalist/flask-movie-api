from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FileField, IntegerField, DateField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired


class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    genres_id = SelectField('Genres', choices=[None])
    release_date = DateField('Release')
    producer_id = SelectField('Producer', choices=[None])
    body = TextAreaField('Body')
    poster = FileField('Image')
    publication = DateField('Publication')
    submit = SubmitField('Add movie')


    # def validate_name(self, name):
    #     user = User.query.filter_by(name=name.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different name.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')


class GenreForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add genre')


class ProducerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    poster = FileField('Image')
    submit = SubmitField('Save')