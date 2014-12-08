from flask import Flask, render_template, request, flash
from forms import SubmitForm
 
app = Flask(__name__) 
 
app.secret_key = 'development key'  

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
      print form.dataFile.data
      print form.trainingMode.data
      print form.trainingData.data
 
      return render_template('submit.html', success=True)
 
  elif request.method == 'GET':
    return render_template('submit.html', form=form)

if __name__ == '__main__':
  app.run(debug=True)