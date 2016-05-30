from flask.ext.wtf import Form
from wtforms import ValidationError, StringField, SubmitField, FileField, TextField, FieldList, TextAreaField
from wtforms.validators import Required, Length
from ..models import User, SRD, Comment, Tag, TagTable, Rating


class SRDForm(Form):
	file = FileField('SRD .pdf', validators=[Required()])
	title = StringField("Title", validators=[Required(), Length(1, 64)])
	tag = FieldList(StringField("Tag"))
	description = TextField("Description", validators=[Required()])
	submit = SubmitField('Submit')
	def validate_title(self, field):
		if SRD.query.filter_by(title=field.data).first():
			raise ValidationError('An SRD with that title has already been submitted')
			
class SRDreForm(Form):
	file = FileField('SRD .pdf', validators=[Required()])
	tag = FieldList(StringField("Tag"))
	description = TextField("Description", validators=[Required()])
	submit = SubmitField('Submit')

class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
