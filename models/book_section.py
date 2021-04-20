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
  
  return render_template('books/home.html', name = session['name'], id = _id, role = role, message="")

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

  
  cur.execute("SELECT DISTINCT shelf_id FROM shelf;")
  rv = cur.fetchall()

  shelves = rv

  mysql.connection.commit()
  cur.close()

  return render_template('books/view-single.html', name = session['name'], id = _id, role = role,  shelf_id = shelf_id, files=files, extra=extra, shelves = shelves)


def books_search_title(title):

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
  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title LIKE '%s%%' "% (title))
  rv = cur.fetchall()
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6, shelf_id 7}
  
  files = sanitize(rv)

  mysql.connection.commit()
  cur.close()

  return render_template('books/search.html', name = session['name'], id = _id, role = role, files=files, search = title)

def view_side_search(search, title):
  
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
  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title LIKE '%s%%' "% (search))
  rv = cur.fetchall()
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6}
  
  files = sanitize(rv)

  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title = '%s' "% (title))
  rv = cur.fetchall()

  extra = sanitize(rv)

  cur.execute("SELECT DISTINCT shelf_id FROM shelf;")
  rv = cur.fetchall()

  shelves = rv

  mysql.connection.commit()
  cur.close()

  return render_template('books/view-single-search.html', name = session['name'], id = _id, role = role,  search = search, files=files, extra=extra, shelves=shelves)
def books_move_to(shelf_id, title):

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
  cur.execute("SELECT count(*) FROM books WHERE shelf_id = '%s';"%(shelf_id))
  rv = cur.fetchall()
  count = rv[0][0]
  cur.execute("SELECT capacity FROM shelf WHERE shelf_id = '%s';"%(shelf_id))
  rv = cur.fetchall()
  mysql.connection.commit()
  cur.close()
  cap = rv[0][0]
  if(count < cap):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE BOOKS SET shelf_id = '%s' WHERE title = '%s';"%(shelf_id, title))
    flash("Success Book Updated!")
    cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication FROM books WHERE shelf_id = '%s' "% (shelf_id))
    rv = cur.fetchall()
    ## {isbn 0, author 1, title 2, rating 3,
    ##  current_status 4, copy 5, year_ 6}

    files = sanitize(rv)

    mysql.connection.commit()
    cur.close()

    return render_template('books/shelf.html', name = session['name'], id = _id, role = role, shelf_id = shelf_id, files=files)
  else:
    flash("Fail Update!")
    if not request.referrer:
      self._error_response('The referrer header is missing.')
    return redirect(request.referrer)
  

def books_list_title(title):
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
  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title = '%s' "% (title))
  rv = cur.fetchall()
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6}

  files = sanitize(rv)

  mysql.connection.commit()
  cur.close()

  return render_template('books/books_list_title.html', name = session['name'], id = _id, role = role, title = title, files=files)


def books_delete(title,isbn):

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
  cur.execute("DELETE FROM BOOKS WHERE isbn = '%s';"%(isbn))
  flash("Success Book Delete!")
  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title = '%s' "% (title))
  rv = cur.fetchall()
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6}

  files = sanitize(rv)

  mysql.connection.commit()
  cur.close()

  return redirect(url_for('books_list_title', name = session['name'], id = _id, role = role, title = title, files=files))

def books_modify(isbn):
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
    print(request.form)
    isbn = request.form['isbn']
    author  = request.form['author']
    title = request.form['title']
    rating= request.form['rating']
    status = request.form['status']
    cn = request.form['cn']
    year = request.form['year']
    shelf_id = request.form['shelf_id']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE books set author='%s', title='%s', rating='%s', current_status='%s', copy_number='%s', year_of_publication='%s', shelf_id='%s' WHERE isbn = '%s' "% (author, title, rating, status, cn, year, shelf_id ,isbn))
    
    cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title = '%s' "% (title))
    rv = cur.fetchall()
    ## {isbn 0, author 1, title 2, rating 3,
    ##  current_status 4, copy 5, year_ 6}

    files = sanitize(rv)

    mysql.connection.commit()
    cur.close()
    flash("Success Book Modified!")

    return redirect(url_for('books_list_title', name = session['name'], id = _id, role = role, title = title, files=files))

    
    
  cur = mysql.connection.cursor()
  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE isbn = '%s' "% (isbn))
  rv = cur.fetchall()
  details = rv[0]
  mysql.connection.commit()
  cur.close()
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6}
  return render_template('books/modify.html', name = session['name'], id = _id, role = role, isbn = isbn, details=details)
