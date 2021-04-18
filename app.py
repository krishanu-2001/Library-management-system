from flask import *
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
import yaml
import hashlib

# modules
import models.librarian_section as librarian_section

app = Flask(__name__)
CORS(app)
app.secret_key = "abc"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

app.add_url_rule('/librarian/login', view_func=librarian_section.librarian_login, methods=['GET','POST'])
app.add_url_rule('/librarian/home', view_func=librarian_section.librarian_home, methods=['GET','POST'])
app.add_url_rule('/librarian/add_librarian', view_func=librarian_section.librarian_add_librarian, methods=['GET','POST'])
app.add_url_rule('/librarian/download_employee', view_func=librarian_section.download_employee, methods=['GET'])
app.add_url_rule('/librarian/add_student', view_func=librarian_section.librarian_add_student, methods=['GET','POST'])
app.add_url_rule('/librarian/download_student', view_func=librarian_section.download_student, methods=['GET','POST'])
app.add_url_rule('/librarian/uploaded_student_files', view_func=librarian_section.uploaded_student_files, methods=['GET','POST'])
app.add_url_rule('/return-files-student/<filename>', view_func=librarian_section.return_files_student, methods=['GET'])
app.add_url_rule('/librarian/uploaded_librarian_files', view_func=librarian_section.uploaded_librarian_files, methods=['GET','POST'])
app.add_url_rule('/return-files-librarian/<filename>', view_func=librarian_section.return_files_librarian, methods=['GET'])

if __name__ == '__main__':
    flag = 0
    app.run(debug=True)
