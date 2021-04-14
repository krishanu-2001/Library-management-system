from flask import *
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
import yaml
import hashlib

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

if __name__ == '__main__':
    flag = 0
    app.run(debug=True)
