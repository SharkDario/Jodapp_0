from flask import Flask, render_template, make_response
import time
from .firebaseConfig import config
from pyrebase import pyrebase

firebase=pyrebase.initialize_app(config)
autenticacion = firebase.auth()
db = firebase.database()


app = Flask(__name__)

def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)

@app.route('/')
def home():
    context = { 'server_time': format_server_time() }
    return render_template('index.html', context=context)

@app.route('/login')
def login():
    return render_template('login.html')

#if __name__ == '__main__':
#    app.run()