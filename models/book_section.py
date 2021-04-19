from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib
import flask_excel as excel
import pyexcel_xlsx
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "abc"
excel.init_excel(app) # required since version 0.0.7

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)



# util function
def debug():
  print("\n\n\n\n\n\n----------------------\n\n\n\n\n\n")






def books_home():

  ### base logic for identifying role
  if session['lid'] == "" and session['sid'] == "":
    return render_template('other/not_logged_in.html')
  if session['lid'] != "":
    _id = session['lid']
  else:
    _id = session['sid']
  role = session['role']
  ### logic ends

  if request.method == 'POST':
    debug()
  
  return render_template('books/home.html', name = session['name'], id = _id, role = role)

