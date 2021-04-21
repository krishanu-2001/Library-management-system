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
  userDetails = rv[0]
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
  u_id = session['uid']
  cur = mysql.connection.cursor()
  cur.execute("SELECT isbn,user.user_id,reading_list.name AS listname,list_url,type,user.name AS user_name FROM library.reading_list JOIN library.user WHERE reading_list.user_id=user.user_id AND user.user_id='%s' GROUP BY list_url"% (u_id))
  rv = cur.fetchall()
  mylists = rv
  cur.execute("SELECT isbn,user.user_id,reading_list.name AS listname,list_url,type,user.name AS user_name FROM library.reading_list JOIN library.user WHERE reading_list.user_id=user.user_id AND user.user_id!='%s' AND type='PUBLIC' GROUP BY list_url"% (u_id))
  rv = cur.fetchall()
  publiclists = rv
  cur.close()
  return render_template('user/readinglist.html', name = session['name'], mylists= mylists, publiclists= publiclists)

def friends():
  if session['uid'] == "":
    return render_template('other/not_logged_in.html')
  if request.method == 'POST':
    data=request.form
    cur = mysql.connection.cursor()
    user_id = session['uid']
    friend_id = data['fid']
    if data['type']=='remove':
      cur.execute("DELETE FROM friend WHERE user_id = '%s' AND friend_id = '%s';"%(user_id, friend_id))
      cur.execute("DELETE FROM friend WHERE user_id = '%s' AND friend_id = '%s';"%(friend_id, user_id))
    elif data['type']=='accept':
      cur.execute("UPDATE friend SET status=1 WHERE user_id = '%s' AND friend_id = '%s';"%(user_id, friend_id))
      cur.execute("INSERT INTO friend (user_id, friend_id, status) VALUES ('%s', '%s', 1);"%(friend_id, user_id))
    elif data['type']=='reject':
      cur.execute("DELETE FROM friend WHERE user_id = '%s' AND friend_id = '%s' AND status=0;"%(user_id, friend_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('friends'))

  u_id = session['uid']
  cur = mysql.connection.cursor()
  cur.execute("SELECT friend.user_id, friend_id, name FROM friend JOIN user WHERE friend.friend_id= user.user_id AND friend.user_id='%s' AND status=1;"% (u_id))
  rv = cur.fetchall()
  friends = rv
  cur.execute("SELECT friend.user_id, friend_id, name FROM friend JOIN user WHERE friend.friend_id= user.user_id AND friend.user_id='%s' AND status=0;"% (u_id))
  rv = cur.fetchall()
  requests = rv
  cur.close()
  return render_template('user/friends.html', name = session['name'], friends=friends, requests=requests)

def add_friend():
  if session['uid'] == "":
    return render_template('other/not_logged_in.html')
  if request.method == 'POST':
    data=request.form
    if data['type']=='query':
      cur = mysql.connection.cursor()
      cur.execute("SELECT user_id, name, role, address FROM user WHERE name='%s' AND user_id != '%s';"%(data['name'],session['uid']))
      rv=cur.fetchall()
      cur.close()
      return jsonify(rv)
    elif data['type']=='add':
      user_id = session['uid']
      friend_id = data['uid']
      cur = mysql.connection.cursor()
      cur.execute("SELECT * FROM friend WHERE user_id = '%s' AND friend_id = '%s' AND status = 0;"%(user_id, friend_id))
      rv=cur.fetchall()
      if len(rv)>0:
        cur.execute("UPDATE friend SET status=1 WHERE user_id = '%s' AND friend_id = '%s';"%(user_id, friend_id))
        cur.execute("INSERT INTO friend (user_id, friend_id, status) VALUES ('%s', '%s', 1);"%(friend_id, user_id))
      else: 
        cur.execute("SELECT * FROM friend WHERE user_id = '%s' AND friend_id = '%s' AND status = 0;"%(friend_id, user_id))
        rv=cur.fetchall()
        if len(rv)==0:
          cur.execute("INSERT INTO friend (user_id, friend_id, status) VALUES ('%s', '%s', 0);"%(friend_id, user_id))
      mysql.connection.commit()
      cur.close()
      return redirect(url_for('friends'))
  return render_template('user/addfriend.html', name = session['name'])

