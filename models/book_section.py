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

def sanitize(rv):
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6}
  files = {}
  for row in rv:
    # segregate by title
    title = row[2]
    if title not in files:
      files[title] = []

    files[title].append(row)
  
  for title in files.keys():
    files[title].sort(key = lambda x: x[4])

  return files


def books_home():

  ### base logic for identifying role
  if 'lid' not in session and 'uid' not in session:
    return render_template('other/not_logged_in.html')
  if 'lid' in session:
    _id = session['lid']
  else:
    _id = session['uid']
  role = session['role']
  ### logic ends

  if request.method == 'POST':
    debug()
  
  return render_template('books/home.html', name = session['name'], id = _id, role = role)

def books_shelf_id(shelf_id):

  ### base logic for identifying role
  if 'lid' not in session and 'uid' not in session:
    return render_template('other/not_logged_in.html')
  if 'lid' in session:
    _id = session['lid']
  else:
    _id = session['uid']
  role = session['role']
  ### logic ends

  cur = mysql.connection.cursor()
  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication FROM books WHERE shelf_id = '%s' "% (shelf_id))
  rv = cur.fetchall()
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6}
  
  files = sanitize(rv)

  print(files)
  debug()
  mysql.connection.commit()
  cur.close()

  return render_template('books/shelf.html', name = session['name'], id = _id, role = role, shelf_id = shelf_id, files=files)

def view_side(shelf_id, title):
  
  ### base logic for identifying role
  if 'lid' not in session and 'uid' not in session:
    return render_template('other/not_logged_in.html')
  if 'lid' in session:
    _id = session['lid']
  else:
    _id = session['uid']
  role = session['role']
  ### logic ends

  if request.method == 'POST':
    debug()
  
  
  cur = mysql.connection.cursor()
  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication FROM books WHERE shelf_id = '%s' "% (shelf_id))
  rv = cur.fetchall()
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6}
  
  files = sanitize(rv)

  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication FROM books WHERE title = '%s' "% (title))
  rv = cur.fetchall()

  extra = sanitize(rv)

  debug()
  mysql.connection.commit()
  cur.close()

  return render_template('books/view-single.html', name = session['name'], id = _id, role = role,  shelf_id = shelf_id, files=files, extra=extra)