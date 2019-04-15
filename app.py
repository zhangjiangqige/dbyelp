from flask import Flask
from flask_cors import CORS

app = Flask("dbyelp")
app.secret_key = 'qiangulubuzhuanhouguluzhuan'
CORS(app)
