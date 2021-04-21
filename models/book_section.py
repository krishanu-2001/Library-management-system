from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib
import flask_excel as excel
import pyexcel_xlsx
import os
from werkzeug.utils import secure_filename
import datetime  

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
    files[title].sort(key = lambda x: x[4], reverse=True)

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

  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication FROM books WHERE title = '%s' AND shelf_id = '%s';"% (title, shelf_id))
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
  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title LIKE '%s%%';"% (search))
  rv = cur.fetchall()
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6}
  
  files = sanitize(rv)

  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title = '%s'; "% (title))
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

def books_rate(title, isbn):
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
    cur = mysql.connection.cursor()
    rating = (request.form['rating'])
    if not rating or type(rating) == 'None':
      rating = '0'
    rating = float(rating)
    review = request.form['review']
    if role[0] != 'l':
      cur.execute("INSERT IGNORE INTO rate (isbn, user_id, rating, review) VALUES ('%s', '%s', %f, '%s');"%(isbn, _id, rating, review))
      cur.execute("UPDATE rate set rating=%f, review='%s' WHERE isbn = '%s' and user_id = '%s';"%(rating, review, isbn, _id))

    #calc rating
    cur.execute("SELECT avg(rating) FROM rate WHERE isbn = '%s';"%(isbn))
    rv = cur.fetchall()
    newRating = (rv[0][0])
    if not newRating or type(newRating) == 'None':
      newRating = 0
    
    newRating = float(newRating)

    cur.execute("UPDATE books set rating=%f WHERE isbn = '%s';"%(newRating, isbn))

    cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title = '%s' "% (title))
    rv = cur.fetchall()
    ## {isbn 0, author 1, title 2, rating 3,
    ##  current_status 4, copy 5, year_ 6}
    files = sanitize(rv)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('books_list_title', name = session['name'], id = _id, role = role, title = title, files=files))
  
  cur = mysql.connection.cursor()
  cur.execute("SELECT isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id FROM books WHERE title = '%s' "% (title))
  rv = cur.fetchall()
  ## {isbn 0, author 1, title 2, rating 3,
  ##  current_status 4, copy 5, year_ 6}
  files = sanitize(rv)
  cur.execute("SELECT user_id, review FROM rate WHERE isbn = '%s';"%(isbn))
  rv = cur.fetchall()
  review = (rv)
  cur.execute("SELECT rating FROM books WHERE isbn = '%s' "% (isbn))
  rv = cur.fetchall()
  rating = rv[0][0]
  mysql.connection.commit()
  cur.close()

  return render_template('books/book_rating.html', name = session['name'], id = _id, role = role, title = title, isbn = isbn, rating = rating, files=files, review=review)

def books_issue(title, isbn):
  if 'uid' not in session:
    return render_template('other/not_logged_in.html')

  user_id = session['uid']
  role = session['role']
  dt = datetime.datetime.now()
  ds = 10
  if role == 'faculty':
    ds= 30
  end_date = dt + datetime.timedelta(days=ds)
  dt=str(dt)
  dt = dt[0:10]

  cur = mysql.connection.cursor()

  cur.execute(''' SELECT count(*) FROM books WHERE user_id='%s' ;'''%(user_id))
  rv = cur.fetchall()
  issued_books = (int)(rv[0][0])

  cur.execute(''' SELECT unpaid_fines FROM user WHERE user_id='%s' ;'''%(user_id))
  rv = cur.fetchall()
  unpaid_fines = (int)(rv[0][0])
  limit = 3
  if role == 'faculty':
    limit = 10
  if issued_books < limit and unpaid_fines < 1000:
    cur.execute(''' SELECT current_status FROM books WHERE isbn='%s' ;'''%(isbn))
    rv = cur.fetchall()
    status = (rv[0][0])
    if status == 'on-shelf':
      flash('Success Request Send!')
      cur.execute(''' UPDATE books SET user_id='%s', issue_date='%s', issue_status='request' WHERE isbn='%s';'''%(user_id, dt, isbn))
    else:
      flash('Book already issued!')
  elif unpaid_fines > 1000:
      flash('Please pay fine!')
  else:
    flash('Books limit exceeded!')

  mysql.connection.commit()
  cur.close()

  return redirect(request.referrer)

def books_hold(title, isbn):
  if 'uid' not in session:
    return render_template('other/not_logged_in.html')

  user_id = session['uid']
  role = session['role']
  dt = datetime.datetime.now()
  ds = 10
  if role == 'faculty':
    ds= 30
  end_date = dt + datetime.timedelta(days=ds)
  dt=str(dt)
  dt = dt[0:10]

  cur = mysql.connection.cursor()

  cur.execute(''' SELECT count(*) FROM books WHERE user_id='%s' ;'''%(user_id))
  rv = cur.fetchall()
  issued_books = (int)(rv[0][0])
  cur.execute(''' SELECT unpaid_fines FROM user WHERE user_id='%s' ;'''%(user_id))
  rv = cur.fetchall()
  unpaid_fines = (int)(rv[0][0])
  limit = 3
  if role == 'faculty':
    limit = 10
  if issued_books < limit and unpaid_fines < 1000:
    cur.execute(''' SELECT current_status FROM books WHERE isbn='%s' ;'''%(isbn))
    rv = cur.fetchall()
    status = (rv[0][0])
    if status == 'on-shelf' or status == 'on-loan':
      flash('Success Request Send!')
      cur.execute(''' INSERT IGNORE INTO HOLD (user_id, isbn, hold_date) VALUES ('%s', '%s', '%s'); '''%(user_id, isbn, dt))
    else:
      flash('Book already on hold!')
  elif unpaid_fines > 1000:
      flash('Please pay fine!')
  else:
    flash('Books limit exceeded!')

  mysql.connection.commit()
  cur.close()

  return redirect(request.referrer)
