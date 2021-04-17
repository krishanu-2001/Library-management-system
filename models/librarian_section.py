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

UPLOAD_FOLDER = 'templates\librarian\employee_forms'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      


      # data base logic
      librarian_details = request.form
      print(librarian_details)
      l_id = librarian_details['id']
      name = librarian_details['name']
      address = librarian_details['address']
      password = "1234"
      cur = mysql.connection.cursor()
      cur.execute('''INSERT INTO librarian (librarian_id, name, address, password)
             VALUES ('%s', '%s', '%s', '%s')'''% (l_id, name, address, password))
      debug()
      mysql.connection.commit()
      cur.close()


      return redirect(url_for('librarian_home', name = session['name'], lid = session['lid']))

  if request.method == 'POST':
    debug()

  return render_template('librarian/add_librarian.html', name = session['name'], lid = session['lid'])

def download_employee():
    try:
      path = os.path.join("templates\other\employee_form.pdf")
      return send_file(path, as_attachment=True)
    except:
      flash("Not Found!")
      return redirect(url_for('librarian_home', name = session['name'], lid = session['lid']))
