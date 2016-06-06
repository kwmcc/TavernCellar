from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from .models import User

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])

    #Attempt to use Whoosh tutorial