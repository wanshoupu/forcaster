from flask.ext.wtf import Form
from wtforms.fields import FileField, TextField, TextAreaField, SubmitField, BooleanField
 
class ContactForm(Form):
  name = FileField("Name")
  email = BooleanField("Email")
  message = TextAreaField("Message")
  submit = SubmitField("Send")