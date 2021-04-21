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

UPLOAD_FOLDER_EMPLOYEE = 'templates\librarian\employee_forms'
UPLOAD_FOLDER_STUDENT = 'templates\librarian\student_forms'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER_EMPLOYEE'] = UPLOAD_FOLDER_EMPLOYEE
app.config['UPLOAD_FOLDER_STUDENT'] = UPLOAD_FOLDER_STUDENT


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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitizeRequest(rv):
  # ('2'- 0, '3'-1, datetime.date(2021, 4, 20)-2,
  #  datetime.date(2021, 4, 20)-3, 'faculty'-4,
  #  'User3'-5, datetime.date(2021, 4, 30)-6
  files = []
  print(rv)
  for rows in rv:
    temp = []
    for i in rows:
      temp.append(i)
    issuedt = rows[2]
    duedt = rows[6]
    dt = datetime.datetime.now().date()
    fines = 0
    delta = dt - duedt
    x = delta.days
    if x < 0:
      x = 0
    fines = x*10
    temp.append(fines)
    files.append(temp)

  files.sort(key = lambda x: x[7], reverse=True)

  return files





def librarian_login():
  if request.method == 'POST':
    librarian_details = request.form
    l_id = librarian_details['lid']
    password = librarian_details['password']
    hashedpassword = hashlib.md5(password.encode()).hexdigest()
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*), password, name FROM librarian WHERE librarian_id = '%s' "% (l_id))
    rv = cur.fetchall()
    flag = (rv[0][0])
    curpassword = (rv[0][1])
    name = (rv[0][2])
    print(rv)
    debug()
    mysql.connection.commit()
    cur.close()
    # access logic
    if (flag >= 1 and password == curpassword):
      if 'uid' in session:
        session.pop('uid')
      session['lid'] = l_id
      session['name'] = name
      session['role'] = 'librarian'
      return redirect(url_for('librarian_home', name = name, lid = l_id))
    else:
      return render_template('librarian/login.html', flag = 0)

  return render_template('librarian/login.html', flag = 1)

def librarian_logout():
  session.pop('lid',None)
  session.pop('name',None)
  session.pop('role',None)
  return redirect(url_for('index'))

def librarian_home():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    debug()
  
  return render_template('librarian/home.html', name = session['name'], lid = session['lid'])

# @app.route('/librarian/tab', methods=['GET', 'POST'])
def librarian_tab_panel():
    if 'lid' not in session:
        return render_template('other/not_logged_in.html')
    if request.method == 'POST':
      debug()
  
    return render_template('librarian/tab-panel.html',  name = session['name'], lid = session['lid'])

# @app.route('/librarian/table', methods=['GET', 'POST'])
def librarian_table():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')
  if request.method == 'POST':
    debug()
  
  return render_template('librarian/table.html',  name = session['name'], lid = session['lid'])


def librarian_add_librarian():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')
  
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER_EMPLOYEE'], filename))
      


      # data base logic
      librarian_details = request.form
      print(librarian_details)
      l_id = librarian_details['id']
      name = librarian_details['name']
      address = librarian_details['address']
      password = "1234"
      cur = mysql.connection.cursor()
      cur.execute('''INSERT INTO librarian (librarian_id, name, address, password, notes)
             VALUES ('%s', '%s', '%s', '%s', '%s')'''% (l_id, name, address, password, filename))
      flash('Success librarian added')
      mysql.connection.commit()
      cur.close()


      return redirect(url_for('librarian_home', name = session['name'], lid = session['lid']))

  return render_template('librarian/add_librarian.html', name = session['name'], lid = session['lid'])

def download_employee():
    try:
      path = os.path.join("templates\other\employee_form.pdf")
      return send_file(path, as_attachment=True)
    except:
      flash("Not Found!")
      return redirect(url_for('librarian_home', name = session['name'], lid = session['lid']))




def librarian_add_student():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')
  
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)

    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER_STUDENT'], filename))
      


      # data base logic
      librarian_details = request.form
      print(librarian_details)
      user_id = librarian_details['id']
      name = librarian_details['name']
      role = librarian_details['role']
      unpaid_fines = 0
      address = librarian_details['address']
      password = "1234"
      cur = mysql.connection.cursor()
      cur.execute('''INSERT INTO user (user_id, name, role, address, password, unpaid_fines, notes)
             VALUES ('%s', '%s', '%s', '%s', '%s', %d, '%s')'''% (user_id, name, role, address, password, unpaid_fines, filename))
      
      shelf_name1 = "Currently_reading"
      shelf_name2 = "Wishlist"
      shelf_name3 = "Already_read"
      cur.execute(''' INSERT IGNORE INTO personal_book_shelf (user_id, shelf_name, shelf_url) VALUES ('%s', '%s', '%s'); '''%(user_id, shelf_name1, user_id+"-"+shelf_name1))
      cur.execute(''' INSERT IGNORE INTO personal_book_shelf (user_id, shelf_name, shelf_url) VALUES ('%s', '%s', '%s'); '''%(user_id, shelf_name2, user_id+"-"+shelf_name2))
      cur.execute(''' INSERT IGNORE INTO personal_book_shelf (user_id, shelf_name, shelf_url) VALUES ('%s', '%s', '%s'); '''%(user_id, shelf_name3, user_id+"-"+shelf_name3))
      
      list1 = "Currently_reading"
      list2 = "Wishlist"
      list3 = "Already_read"
      cur.execute(''' INSERT IGNORE INTO reading_list (user_id, name, list_url, type) VALUES ('%s', '%s', '%s', '%s'); '''%(user_id, list1, user_id+"-"+list1, 'public'))
      cur.execute(''' INSERT IGNORE INTO reading_list (user_id, name, list_url, type) VALUES ('%s', '%s', '%s', '%s'); '''%(user_id, list2, user_id+"-"+list2, 'private'))
      cur.execute(''' INSERT IGNORE INTO reading_list (user_id, name, list_url, type) VALUES ('%s', '%s', '%s', '%s'); '''%(user_id, list3, user_id+"-"+list3, 'public'))
      

      mysql.connection.commit()
      cur.close()
      flash('Success student/Faculty added')
      return redirect(url_for('librarian_home', name = session['name'], lid = session['lid']))

  return render_template('librarian/add_student.html', name = session['name'], lid = session['lid'])

def download_student():
  try:
    path = os.path.join("templates\other\student_form.pdf")
    return send_file(path, as_attachment=True)
  except:
    flash("Not Found!")
    return redirect(url_for('librarian_home', name = session['name'], lid = session['lid']))

def uploaded_student_files():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  path =app.config['UPLOAD_FOLDER_STUDENT']
  cur = mysql.connection.cursor()
  cur.execute('''SELECT user_id, name, notes
               FROM user WHERE role = "student"; ''')
  rv = cur.fetchall()
  files = rv

  finalFiles = []
  for items in files:
    if items[2] == None: continue
    # f1 = os.path.join(path, items[2])
    f1 = items[2]
    finalFiles.append([items[0], items[1], f1])

  mysql.connection.commit()
  cur.close()


  # faculty
  cur = mysql.connection.cursor()
  cur.execute('''SELECT user_id, name, notes
               FROM user WHERE role = "faculty"; ''')
  cv = cur.fetchall()
  files2 = cv

  finalFiles2 = []
  for items in files2:
    if items[2] == None: continue
    # f1 = os.path.join(path, items[2])
    f1 = items[2]
    finalFiles2.append([items[0], items[1], f1])

  mysql.connection.commit()
  cur.close()

  # FOR ALL FILES   
  # for filename in os.listdir(path):
  #   if filename.endswith(".pdf"):
  #     f1 = os.path.join(path, filename)
  #     print(f1)
  #     files.append(f1)
  
  return render_template('librarian/uploaded_student_files.html', filesS = finalFiles
        , filesF = finalFiles2, name = session['name'], lid = session['lid'])

def return_files_student(filename):
    file_path = os.path.join(UPLOAD_FOLDER_STUDENT, filename)
    return send_file(file_path, as_attachment=True, attachment_filename='')

def uploaded_librarian_files():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  path =app.config['UPLOAD_FOLDER_STUDENT']
  cur = mysql.connection.cursor()
  cur.execute('''SELECT librarian_id, name, notes
               FROM librarian; ''')
  rv = cur.fetchall()
  files = rv
  finalFiles = []
  for items in files:
    if items[2] == None: continue
    # f1 = os.path.join(path, items[2])
    f1 = items[2]
    finalFiles.append([items[0], items[1], f1])

  mysql.connection.commit()
  cur.close()
  # FOR ALL FILES   
  # for filename in os.listdir(path):
  #   if filename.endswith(".pdf"):
  #     f1 = os.path.join(path, filename)
  #     print(f1)
  #     files.append(f1)
  
  return render_template('librarian/uploaded_librarian_files.html', files = finalFiles, name = session['name'], lid = session['lid'])

def return_files_librarian(filename):
    file_path = os.path.join(UPLOAD_FOLDER_EMPLOYEE, filename)
    return send_file(file_path, as_attachment=True, attachment_filename='')

def delete_student_forms(sid):
  cur = mysql.connection.cursor()
  cur.execute('''DELETE FROM user where user_id = '%s';'''%(sid))
  mysql.connection.commit()
  cur.close()
  return redirect(url_for('uploaded_student_files', name = session['name'], lid = session['lid']))

def delete_librarian_forms(lid):
  cur = mysql.connection.cursor()
  cur.execute('''DELETE FROM librarian where librarian_id = '%s';'''%(lid))
  mysql.connection.commit()
  cur.close()
  return redirect(url_for('uploaded_librarian_files', name = session['name'], lid = session['lid']))

def librarian_add_books():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')
  
  if request.method == 'POST':
    # data base logic
    book_details = request.form
    isbn = book_details['isbn']
    title = book_details['title']
    author = book_details['author']
    year = (book_details['year'])
    if year == "" or type(year) == "None":
      year = 2021
    year = (int)(year)
    shelf_id= (book_details['shelf_id'])
    copy_number= book_details['copy_number']
    if copy_number == "" or type(copy_number) == "None":
      copy_number = 2021
    copy_number = (int)(copy_number)
    rating = 0
    current_status = 'on-shelf'

    cur = mysql.connection.cursor()
    cur.execute('''INSERT IGNORE INTO books (isbn, author, title, rating, current_status, copy_number, year_of_publication, shelf_id) 
    VALUES ('%s', '%s', '%s', %f, '%s', %d, %d, '%s');
    '''%(isbn, author, title, rating, current_status, copy_number, year, shelf_id))
    mysql.connection.commit()
    cur.close()
    flash('Success Book Added!')
    return redirect(url_for('librarian_home', name = session['name'], lid = session['lid']))

  return render_template('/librarian/add_books.html', name = session['name'], lid = session['lid'])


def librarian_add_shelf():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')
  
  if request.method == 'POST':
    # data base logic
    shelf_details = request.form
    shelf_id = shelf_details['shelf_id']
    capacity = shelf_details['capacity']
    if capacity == "" or type(capacity) == "None":
      capacity = 2
    capacity = (int)(capacity)
    cur = mysql.connection.cursor()
    cur.execute('''INSERT IGNORE INTO shelf (shelf_id, capacity) VALUES
      ('%s', %d);
    '''%(shelf_id,  capacity))
    mysql.connection.commit()
    cur.close()
    flash('Success shelf added')
    return redirect(url_for('librarian_home', name = session['name'], lid = session['lid']))

  return render_template('/librarian/add_shelf.html', name = session['name'], lid = session['lid'])

def librarian_requests():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  cur = mysql.connection.cursor()
  
  cur.execute(''' 
  SELECT 
      A.isbn,
      A.user_id,
      A.hold_date,
      A.hold_email_date,
      A.hold_status,
      B.issued_books,
      A.role
  FROM
      (SELECT 
          isbn, hold.user_id, hold_date, hold_email_date, hold_status, role
      FROM
          hold, user
      WHERE
          hold.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          books.user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY books.user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.hold_status = 'PENDING'
  ORDER BY A.hold_date DESC;
  ''')
  rv = cur.fetchall()
  requests_hold_pending = rv

  cur.execute('''SELECT 
      A.isbn, A.user_id, A.issue_status, B.issued_books, A.role
  FROM
      (SELECT 
          books.isbn, books.user_id, books.issue_status, books.issue_date, user.role
      FROM
          books, user
      WHERE
          books.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.issue_status = 'request'
  ORDER BY A.issue_date ASC;''')

  rv = cur.fetchall()
  requests_issue_pending = rv


  mysql.connection.commit()
  cur.close()

  return render_template('/librarian/all_requests.html', name = session['name'], lid = session['lid'], requests_hold_pending=requests_hold_pending, requests_issue_pending=requests_issue_pending)

def deny_hold(user_id, isbn):
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  # deny logic here
  cur = mysql.connection.cursor()
  cur.execute("DELETE FROM HOLD WHERE user_id='%s' and isbn='%s' ;"%(user_id, isbn))
  mysql.connection.commit()
  cur.close()

  flash('Success Deny Hold')
  cur = mysql.connection.cursor()
  
  cur.execute(''' 
  SELECT 
      A.isbn,
      A.user_id,
      A.hold_date,
      A.hold_email_date,
      A.hold_status,
      B.issued_books,
      A.role
  FROM
      (SELECT 
          isbn, hold.user_id, hold_date, hold_email_date, hold_status, role
      FROM
          hold, user
      WHERE
          hold.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          books.user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY books.user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.hold_status = 'PENDING'
  ORDER BY A.hold_date DESC;
  ''')
  rv = cur.fetchall()
  requests_hold_pending = sanitizeRequest(rv)

  cur.execute('''SELECT 
      A.isbn, A.user_id, A.issue_status, B.issued_books, A.role
  FROM
      (SELECT 
          books.isbn, books.user_id, books.issue_status, books.issue_date, user.role
      FROM
          books, user
      WHERE
          books.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.issue_status = 'request'
  ORDER BY A.issue_date ASC;''')

  rv = cur.fetchall()
  requests_issue_pending = sanitizeRequest(rv)


  mysql.connection.commit()
  cur.close()

  return redirect(url_for('librarian_requests', name = session['name'], lid = session['lid'], requests_hold_pending=requests_hold_pending, requests_issue_pending=requests_issue_pending))

def deny_issue(user_id, isbn):
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  # deny logic here
  cur = mysql.connection.cursor()
  cur.execute("UPDATE BOOKs SET user_id=NULL, issue_date=NULL, issue_email_date=NULL, issue_status=NULL WHERE user_id='%s' and isbn='%s' ;"%(user_id, isbn))
  mysql.connection.commit()
  cur.close()

  flash('Success Deny Issue')
  cur = mysql.connection.cursor()
  
  cur.execute(''' 
  SELECT 
      A.isbn,
      A.user_id,
      A.hold_date,
      A.hold_email_date,
      A.hold_status,
      B.issued_books,
      A.role
  FROM
      (SELECT 
          isbn, hold.user_id, hold_date, hold_email_date, hold_status, role
      FROM
          hold, user
      WHERE
          hold.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          books.user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY books.user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.hold_status = 'PENDING'
  ORDER BY A.hold_date DESC;
  ''')
  rv = cur.fetchall()
  requests_hold_pending = sanitizeRequest(rv)

  cur.execute('''SELECT 
      A.isbn, A.user_id, A.issue_status, B.issued_books, A.role
  FROM
      (SELECT 
          books.isbn, books.user_id, books.issue_status, books.issue_date, user.role
      FROM
          books, user
      WHERE
          books.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.issue_status = 'request'
  ORDER BY A.issue_date ASC;''')

  rv = cur.fetchall()
  requests_issue_pending = sanitizeRequest(rv)


  mysql.connection.commit()
  cur.close()

  return redirect(url_for('librarian_requests', name = session['name'], lid = session['lid'], requests_hold_pending=requests_hold_pending, requests_issue_pending=requests_issue_pending))

def accept_issue(role, user_id, isbn):
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  # deny logic here
  cur = mysql.connection.cursor()
  dt = datetime.datetime.now()
  ds = 10
  if role == 'faculty':
    ds = 30
  edt = dt + datetime.timedelta(days=ds)
  dt = str(dt)
  dt = dt[0:10]
  edt = str(edt)
  edt = edt[0:10]
  cur.execute("UPDATE BOOKS SET user_id=user_id, due_date='%s', issue_date='%s', issue_email_date=NULL, issue_status='issued', current_status='on-loan' WHERE user_id='%s' and isbn='%s' ;"%(edt, dt,user_id, isbn))
  mysql.connection.commit()
  cur.close()

  flash('Success Issued Book!')
  cur = mysql.connection.cursor()
  
  cur.execute(''' 
  SELECT 
      A.isbn,
      A.user_id,
      A.hold_date,
      A.hold_email_date,
      A.hold_status,
      B.issued_books,
      A.role
  FROM
      (SELECT 
          isbn, hold.user_id, hold_date, hold_email_date, hold_status, role
      FROM
          hold, user
      WHERE
          hold.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          books.user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY books.user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.hold_status = 'PENDING'
  ORDER BY A.hold_date DESC;
  ''')
  rv = cur.fetchall()
  requests_hold_pending = sanitizeRequest(rv)

  cur.execute('''SELECT 
      A.isbn, A.user_id, A.issue_status, B.issued_books, A.role
  FROM
      (SELECT 
          books.isbn, books.user_id, books.issue_status, books.issue_date, user.role
      FROM
          books, user
      WHERE
          books.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.issue_status = 'request'
  ORDER BY A.issue_date ASC;''')

  rv = cur.fetchall()
  requests_issue_pending = sanitizeRequest(rv)


  mysql.connection.commit()
  cur.close()

  return redirect(url_for('librarian_requests', name = session['name'], lid = session['lid'], requests_hold_pending=requests_hold_pending, requests_issue_pending=requests_issue_pending))

def accept_hold(user_id, isbn):
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  # deny logic here
  cur = mysql.connection.cursor()
  dt = datetime.datetime.now()
  ds = 10
  dt=str(dt)
  dt = dt[0:10]
  cur.execute("UPDATE HOLD SET hold_date='%s', hold_email_date=NULL, hold_status='ACCEPTED' WHERE user_id='%s' and isbn='%s' ;"%(dt,user_id, isbn))
  cur.execute(''' SELECT current_status FROM books WHERE isbn = '%s';'''%(isbn))
  rv = cur.fetchall()
  status = rv[0][0]
  new_status = 'on-loan-and-on-hold'
  if status == 'on-shelf':
     new_status = 'on-hold'
  cur.execute(''' UPDATE books set current_status = '%s' WHERE isbn = '%s';'''%(new_status, isbn))
  mysql.connection.commit()
  cur.close()

  flash('Success Accepted Hold!')
  cur = mysql.connection.cursor()
  
  cur.execute(''' 
  SELECT 
      A.isbn,
      A.user_id,
      A.hold_date,
      A.hold_email_date,
      A.hold_status,
      B.issued_books,
      A.role
  FROM
      (SELECT 
          isbn, hold.user_id, hold_date, hold_email_date, hold_status, role
      FROM
          hold, user
      WHERE
          hold.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          books.user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY books.user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.hold_status = 'PENDING'
  ORDER BY A.hold_date DESC;
  ''')
  rv = cur.fetchall()
  requests_hold_pending = sanitizeRequest(rv)

  cur.execute('''SELECT 
      A.isbn, A.user_id, A.issue_status, B.issued_books, A.role
  FROM
      (SELECT 
          books.isbn, books.user_id, books.issue_status, books.issue_date, user.role
      FROM
          books, user
      WHERE
          books.user_id = user.user_id) AS A
          LEFT JOIN
      (SELECT 
          user_id, COUNT(*) AS issued_books
      FROM
          books
      GROUP BY user_id) AS B ON A.user_id = B.user_id
  WHERE
      A.issue_status = 'request'
  ORDER BY A.issue_date ASC;''')

  rv = cur.fetchall()
  requests_issue_pending = sanitizeRequest(rv)


  mysql.connection.commit()
  cur.close()

  return redirect(url_for('librarian_requests', name = session['name'], lid = session['lid'], requests_hold_pending=requests_hold_pending, requests_issue_pending=requests_issue_pending))

def librarian_manage():
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  cur = mysql.connection.cursor()
  
  cur.execute(''' 
  SELECT 
      A.isbn,
      A.user_id,
      A.hold_date,
      A.hold_email_date,
	    B.role,
      B.name
  FROM
	hold as A, user as B
      WHERE
		A.user_id = B.user_id
	AND
      A.hold_status = 'PENDING'
  ORDER BY A.hold_date DESC;
  ''')
  rv = cur.fetchall()
  requests_hold_pending = rv
  cur.execute('''SELECT 
    A.isbn, A.user_id, A.issue_date,  A.issue_email_date, B.role, B.name, A.due_date
  FROM
    books as A,
    user as B
  WHERE
    A.user_id = B.user_id
        AND A.issue_status = 'issued'
  ORDER BY A.issue_date DESC;''')

  rv = cur.fetchall()
  requests_issue_pending = sanitizeRequest(rv)


  mysql.connection.commit()
  cur.close()

  return render_template('/librarian/manage.html', name = session['name'], lid = session['lid'], requests_hold_pending=requests_hold_pending, requests_issue_pending=requests_issue_pending)

def delete_return_hold(user_id, isbn):
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')
  cur = mysql.connection.cursor()
  
  cur.execute('''DELETE FROM hold WHERE user_id='%s' and isbn='%s';'''%(user_id, isbn))

  cur.execute(''' 
  SELECT 
      A.isbn,
      A.user_id,
      A.hold_date,
      A.hold_email_date,
	    B.role,
      B.name
  FROM
	hold as A, user as B
      WHERE
		A.user_id = B.user_id
	AND
      A.hold_status = 'PENDING'
  ORDER BY A.hold_date DESC;
  ''')
  rv = cur.fetchall()
  requests_hold_pending = rv
  cur.execute('''SELECT 
    A.isbn, A.user_id, A.issue_date,  A.issue_email_date, B.role, B.name, A.due_date
  FROM
    books as A,
    user as B
  WHERE
    A.user_id = B.user_id
        AND A.issue_status = 'issued'
  ORDER BY A.issue_date DESC;''')

  rv = cur.fetchall()
  requests_issue_pending = sanitizeRequest(rv)


  mysql.connection.commit()
  cur.close()

  return redirect(url_for('librarian_manage', name = session['name'], lid = session['lid'], requests_hold_pending=requests_hold_pending, requests_issue_pending=requests_issue_pending))

def delete_return_issue(user_id, isbn):
  if 'lid' not in session:
    return render_template('other/not_logged_in.html')

  cur = mysql.connection.cursor()

  cur.execute(''' 
  SELECT 
      A.isbn,
      A.user_id,
      A.hold_date,
      A.hold_email_date,
      B.role,
      B.name
  FROM
  hold as A, user as B
      WHERE
    A.user_id = B.user_id
  AND
      A.hold_status = 'PENDING'
  ORDER BY A.hold_date DESC;
  ''')
  rv = cur.fetchall()
  requests_hold_pending = rv
  cur.execute('''SELECT 
    A.isbn, A.user_id, A.issue_date,  A.issue_email_date, B.role, B.name, A.due_date
  FROM
    books as A,
    user as B
  WHERE
    A.user_id = B.user_id
        AND A.issue_status = 'issued'
  ORDER BY A.issue_date DESC;''')

  rv = cur.fetchall()
  requests_issue_pending = sanitizeRequest(rv)

  mysql.connection.commit()
  cur.close()

  if request.method == 'POST':
    cur = mysql.connection.cursor()

    extra = request.form['fine']

    extra = (int)(extra)

    cur.execute('''UPDATE BOOKs SET user_id=NULL, current_status='on-shelf', 
    issue_date=NULL, issue_email_date=NULL, issue_status=NULL 
    WHERE user_id='%s' and isbn='%s';
    '''%(user_id, isbn))

    cur.execute("UPDATE user set unpaid_fines = unpaid_fines + %d where user_id = '%s'"%(extra, user_id))

    mysql.connection.commit()
    cur.close()
    flash('Success Deleted Issue!')

    return redirect(url_for('librarian_manage', name = session['name'], lid = session['lid'], requests_hold_pending=requests_hold_pending, requests_issue_pending=requests_issue_pending))

  return render_template('/librarian/delete_fine.html', name = session['name'], lid = session['lid'], requests_hold_pending=requests_hold_pending, requests_issue_pending=requests_issue_pending)

def reload():
  cur = mysql.connection.cursor()
  dt = datetime.datetime.now().date()

  cur.execute('''UPDATE user set unpaid_fines = 0 WHERE user_id;''')

  cur.execute('''Select isbn, user_id, issue_date, due_date, issue_email_date From Books WHERE user_id AND due_date AND issue_status = 'issued';''')
  rv = cur.fetchall()
  # user_id, issuedate, duedate, emaildate
  for (isbn, user_id, issue_date, due_date, issue_email_date) in rv:
    delta = dt-due_date
    x = delta.days
    if x < 0:
      x = 0

    cur.execute('''UPDATE user set unpaid_fines = unpaid_fines + %d WHERE user_id = '%s';'''%(x*10, user_id))

    y = delta.days
    if y > -5:
      note = 'Please return Book!'
      cur.execute(''' Update Books set notes = '%s', issue_email_date='%s' where isbn = '%s' ;'''%(note, dt,isbn))

  mysql.connection.commit()
  cur.close()
  flash('Success Refreshed Database!')
  

  return redirect(request.referrer)

