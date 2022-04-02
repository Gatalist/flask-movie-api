from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FileField, IntegerField, DateField, SelectField, TextAreaField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired


class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    genres_id = SelectMultipleField('Genres_id', choices=[None])
    release_date = DateField('Release')
    rating_id = SelectField('Rating', choices=[None])
    producer_id = SelectField('Producer', choices=[None])
    body = TextAreaField('Body')
    poster = FileField('Image')
    publication = DateField('Publication')
    submit = SubmitField('Save')


class GenreForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')


class ProducerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    poster = FileField('Image')
    submit = SubmitField('Save')

class StarForm(FlaskForm):
    value = IntegerField('star', validators=[DataRequired()])
    submit = SubmitField('Save')