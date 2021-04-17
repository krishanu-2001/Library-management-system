from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib
import flask_excel as excel
import pyexcel_xlsx

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
