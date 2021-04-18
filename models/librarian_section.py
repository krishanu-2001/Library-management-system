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
      session['lid'] = l_id
      session['name'] = name
      return redirect(url_for('librarian_home', name = name, lid = l_id))
    else:
      return render_template('librarian/login.html', flag = 0)

  return render_template('librarian/login.html', flag = 1)

def librarian_home():
  if session['lid'] == "":
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    debug()
  
  return render_template('librarian/home.html', name = session['name'], lid = session['lid'])

def librarian_add_librarian():
  if session['lid'] == "":
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
      debug()
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
  if session['lid'] == "":
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
      debug()
      mysql.connection.commit()
      cur.close()

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
