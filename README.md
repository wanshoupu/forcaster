This project is for uber demand prediction chanllenge

================================
How to start the web server
================================

Follow these steps to start the web server

Make sure virtual environment is installed 

Let venv manages the project

    virtualenv forcaster


Go to the project root dir

start the virtual environment
    . venv/bin/activate

install Flask, WTF, matplotlib, numpy, and scikit
    pip install Flask flask-wtf matplotlib
    pip install -U numpy scipy scikit-learn

Then the server app
    python app.py
