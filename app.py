from flask import Flask, render_template, request, flash
from forms import SubmitForm
import logging
from logging.handlers import RotatingFileHandler
from training import Trainer
from analyzer import parseJson,plot,groupByHour
from datetime import datetime as dt

UPLOAD_FOLDER = 'resources'

import os
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__, static_url_path = '', static_folder = UPLOAD_FOLDER)
app.secret_key = 'development key'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

trainer = Trainer(app)
timestampes = []

@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/predict')
def predict():
  truncHours = [dt(2012, 4, 30, 10, 0), dt(2012, 4, 30, 22, 0)]
  predictions = trainer.predict(truncHours)
  app.logger.info('predictions:')
  app.logger.info(predictions)
  return render_template('predict.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
  global timestampes
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

      if trainingdata :
        timestampes = parseJson(trainingdata)
        img1, img2 = trainer.train(timestampes)

      return render_template('submit.html', success=True, img1=img1, img2=img2)
 
  elif request.method == 'GET':
    return render_template('submit.html', form=form)

if __name__ == '__main__':
  handler = RotatingFileHandler('/tmp/foo.log', maxBytes=10000, backupCount=1)
  handler.setLevel(logging.INFO)
  app.logger.addHandler(handler)

  app.run(debug=True)