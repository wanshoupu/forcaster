from flask.ext.wtf import Form
from wtforms.fields import FileField, TextField, TextAreaField, SubmitField, BooleanField
 
class SubmitForm(Form):
  dataFile = FileField("Data file")
  trainingMode = BooleanField("Training mode")
  trainingData = TextAreaField("Training data")
  submit = SubmitField("Submit")