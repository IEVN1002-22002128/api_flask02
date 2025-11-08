from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import config

app = Flask(__name__)
app.run(debug=True)
app.config.from_object(config['development'])
mysql = MySQL(app)

CORS(app)

