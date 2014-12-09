from flask import Flask, render_template, request, flash
from forms import SubmitForm
import logging
from logging.handlers import RotatingFileHandler

UPLOAD_FOLDER = '~/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'json'])

app = Flask(__name__) 
app.secret_key = 'development key'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/predict')
def predict():
  return render_template('predict.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
  form = SubmitForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('submit.html', form=form)
    else:
      trainingdata = ''
      if form.dataFile.data :
        trainingdata += request.files[form.dataFile.name].read()
      if form.trainingData.data :
        trainingdata += form.trainingData.data
#      app.logger.info(trainingdata)
 
      return render_template('submit.html', success=True)
 
  elif request.method == 'GET':
    return render_template('submit.html', form=form)

if __name__ == '__main__':
  handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
  handler.setLevel(logging.INFO)
  app.logger.addHandler(handler)
  app.run(debug=True)