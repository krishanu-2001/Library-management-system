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


def user_login():
  if request.method == 'POST':
    user_details = request.form
    u_id = user_details['uid']
    password = user_details['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*), password, name, role FROM user WHERE user_id = '%s' "% (u_id))
    rv = cur.fetchall()
    flag = (rv[0][0])
    curpassword = (rv[0][1])
    name = (rv[0][2])
    role = (rv[0][3])
    print(rv)
    debug()
    mysql.connection.commit()
    cur.close()
    # access logic
    if (flag >= 1 and password == curpassword):
      if 'lid' in session:
        session.pop('lid')
      session['uid'] = u_id
      session['name'] = name
      session['role'] = role
      return redirect(url_for('user_home'))
    else:
      return render_template('user/login.html', flag = 0)

  return render_template('user/login.html', flag = 1)

def user_home():
  if session['uid'] == "":
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    debug()
  u_id = session['uid']
  cur = mysql.connection.cursor()
  cur.execute("SELECT name, role, unpaid_fines FROM user WHERE user_id = '%s' "% (u_id))
  rv = cur.fetchall()
  userDetails=rv[0]
  cur.close()
  return render_template('user/home.html', name = session['name'], userDetails=userDetails)

def browse():
  if session['uid'] == "":
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    debug()
  return render_template('user/browse.html', name = session['name'])

def reading_lists():
  if session['uid'] == "":
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    debug()
  return render_template('user/readinglist.html', name = session['name'])

