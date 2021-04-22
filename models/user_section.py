from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib
import flask_excel as excel
import pyexcel_xlsx
import os
import secrets
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

def user_logout():
  session.pop('uid',None)
  session.pop('name',None)
  session.pop('role',None)
  return redirect(url_for('index'))

def user_home():
  if 'uid' not in session:
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    data=request.form
    cur = mysql.connection.cursor()
    user_id = session['uid']
    isbn = data['isbn']
    cur.execute("UPDATE books SET issue_status='returnrequested' WHERE isbn ='%s' AND user_id='%s'"%(isbn,user_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('user_home'))
  u_id = session['uid']
  cur = mysql.connection.cursor()
  cur.execute("SELECT name, role, unpaid_fines FROM user WHERE user_id = '%s' "% (u_id))
  rv = cur.fetchall()
  userDetails = rv[0]
  cur.execute("SELECT count(personal_book_shelf.shelf_name),personal_book_shelf.shelf_name FROM personal_book_shelf JOIN personal_book_shelf_contains WHERE personal_book_shelf.shelf_url = personal_book_shelf_contains.shelf_url AND user_id = '%s' GROUP BY shelf_name;"%(u_id))
  rv=cur.fetchall()
  bookshelves= rv
  cur.execute("SELECT isbn,title,author,copy_number,issue_date,due_date,issue_status FROM library.books WHERE user_id='%s' AND (issue_status='issued' OR issue_status='returnrequested');"%(u_id))
  rv=cur.fetchall()
  issued = rv
  cur.execute("SELECT books.isbn, books.title, books.author, hold.hold_date, hold.hold_status FROM hold JOIN books WHERE hold.isbn = books.isbn and hold.user_id= '%s';"%(u_id))
  rv=cur.fetchall()
  holds=rv
  cur.close()
  return render_template('user/home.html', name = session['name'], userDetails=userDetails, bookshelves=bookshelves, issued=issued,holds=holds)

def reading_lists():
  if 'uid' not in session:
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    data=request.form
    cur = mysql.connection.cursor()
    user_id = session['uid']
    if data['type']=='add':
      cur.execute("SELECT * from reading_list WHERE user_id='%s' AND name='%s'"%(user_id, data['listname']))
      rv=cur.fetchall()
      if(len(rv)>0):
        flash('Same name can not be used!')
      else: 
        cur.execute("INSERT INTO reading_list (user_id, name, list_url, type) VALUES ('%s', '%s', '%s', '%s')"%(user_id, data['listname'], secrets.token_hex(20), data['access']))
    elif data['type']=='delete':
      cur.execute("DELETE FROM reading_list WHERE list_url='%s';"%(data['url']))
    elif data['type']=='follow':
      cur.execute("INSERT INTO follow (list_url, user_id) VALUES ('%s', '%s')"%(data['url'], user_id))
    elif data['type']=='unfollow':
      cur.execute("DELETE FROM follow WHERE user_id = '%s' AND list_url = '%s';"%(user_id, data['url']))
      print("DELETE FROM follow WHERE user_id = '%s' AND list_url = '%s';"%(user_id, data['url']))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('reading_lists'))
  u_id = session['uid']
  cur = mysql.connection.cursor()
  cur.execute("SELECT reading_list.name AS listname,list_url,type FROM library.reading_list WHERE user_id='%s'"% (u_id))
  rv = cur.fetchall()
  mylists = rv
  cur.execute("SELECT reading_list.name AS listname,list_url,user.name as user_name FROM library.reading_list JOIN library.user WHERE reading_list.user_id=user.user_id AND reading_list.user_id !='%s' AND type = 'PUBLIC'"% (u_id))
  rv = cur.fetchall()
  publiclists = rv
  cur.execute("SELECT list_url FROM library.follow WHERE user_id ='%s'"% (u_id))
  rv = cur.fetchall()
  followcheck = rv
  checklist = []
  for i in range (len(followcheck)):
    checklist.append(followcheck[i][0])
  followed=[]
  for i in range (len(publiclists)):
    if publiclists[i][1] in checklist:
      followed.append(1)
    else:
      followed.append(0) 
  cur.execute("SELECT follow.user_id as followerid, reading_list.user_id as creatorid,reading_list.list_url, reading_list.name as listname, user.name as creatorname FROM library.follow JOIN library.reading_list JOIN library.user WHERE reading_list.user_id=user.user_id AND follow.list_url = reading_list.list_url AND follow.user_id='%s'"% (u_id))
  rv = cur.fetchall()
  followlist = rv
  cur.close()
  return render_template('user/readinglist.html', name = session['name'], mylists= mylists, publiclists= publiclists, followed=followed, followlist= followlist)

def view_reading_list(url):
  if 'uid' not in session:
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    data=request.form
    cur = mysql.connection.cursor()
    isbn = data['isbn']
    if data['type']=='delete':
      cur.execute("DELETE FROM reading_list_contains WHERE isbn='%s' AND list_url='%s'"%(isbn,url))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('view_reading_list',url=url))
  u_id = session['uid']
  cur = mysql.connection.cursor()
  cur.execute("SELECT name,type,user_id from reading_list WHERE list_url='%s'"%(url))
  rv = cur.fetchall()
  listdetail=rv[0]
  delete_status=0
  if(listdetail[2]==u_id):
    delete_status=1
  cur.execute("SELECT books.isbn, books.title, books.author, books.rating, books.year_of_publication FROM reading_list_contains JOIN books WHERE reading_list_contains.isbn = books.isbn AND reading_list_contains.list_url = '%s'"% (url))
  rv = cur.fetchall()
  listbooks = rv
  cur.close()
  return render_template('user/viewreadinglist.html', name = session['name'],listdetail=listdetail,listbooks=listbooks,delete_status=delete_status)


def friends():
  if 'uid' not in session:
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
  if 'uid' not in session:
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

def friend_currentlyreading(id):
  if 'uid' not in session:
    return render_template('other/not_logged_in.html')
  if request.method == 'POST':
    debug()
  cur = mysql.connection.cursor()
  cur.execute("SELECT books.isbn, books.title, books.author, books.rating, books.year_of_publication FROM personal_book_shelf JOIN personal_book_shelf_contains JOIN Books WHERE personal_book_shelf.shelf_url =  personal_book_shelf_contains.shelf_url AND personal_book_shelf_contains.isbn = books.isbn AND personal_book_shelf.user_id= '%s';"%(id))
  rv = cur.fetchall()
  crbooks = rv
  cur.execute("SELECT name,role FROM user WHERE user_id='%s'"%(id))
  rv=cur.fetchall()
  friendDetails=rv
  return render_template('user/currentlyreading.html', name = session['name'], crbooks = crbooks, friendDetails=friendDetails)

def bookshelves():
  if 'uid' not in session:
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    data=request.form
    cur = mysql.connection.cursor()
    user_id = session['uid']
    if data['type']=='add':
      cur.execute("SELECT * from personal_book_shelf WHERE user_id='%s' AND shelf_name='%s'"%(user_id, data['shelf_name']))
      rv=cur.fetchall()
      if(len(rv)>0):
        flash('Same name can not be used!')
      else: 
        cur.execute("INSERT INTO personal_book_shelf (user_id, shelf_name, shelf_url) VALUES ('%s', '%s', '%s')"%(user_id, data['shelf_name'], secrets.token_hex(20)))
    elif data['type']=='delete':
      if(data['name']!='Read' and data['name']!='Currently Reading' and data['name']!='Want to Read'):
        cur.execute("DELETE FROM personal_book_shelf WHERE shelf_url='%s';"%(data['url']))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('bookshelves'))
  u_id = session['uid']
  cur = mysql.connection.cursor()
  cur.execute("SELECT shelf_name ,shelf_url FROM library.personal_book_shelf WHERE user_id='%s'"% (u_id))
  rv = cur.fetchall()
  myshelves = rv 
  cur.close()
  return render_template('user/bookshelves.html', name = session['name'], myshelves= myshelves)

def view_personal_bookshelves(url):
  if 'uid' not in session:
    return render_template('other/not_logged_in.html')

  if request.method == 'POST':
    data=request.form
    cur = mysql.connection.cursor()
    isbn = data['isbn']
    if data['type']=='delete':
      cur.execute("DELETE FROM personal_book_shelf_contains WHERE isbn='%s' AND shelf_url='%s'"%(isbn,url))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('view_personal_bookshelves',url=url))
  u_id = session['uid']
  cur = mysql.connection.cursor()
  cur.execute("SELECT shelf_name from personal_book_shelf WHERE shelf_url='%s'"%(url))
  rv = cur.fetchall()
  shelfdetail=rv[0]
  cur.execute("SELECT books.isbn, books.title, books.author, books.rating, books.year_of_publication FROM personal_book_shelf_contains JOIN books WHERE personal_book_shelf_contains.isbn = books.isbn AND personal_book_shelf_contains.shelf_url = '%s'"% (url))
  rv = cur.fetchall()
  bookshelfbooks = rv
  cur.close()
  return render_template('user/viewpersonalbookshelf.html', name = session['name'],shelfdetail=shelfdetail,bookshelfbooks=bookshelfbooks)