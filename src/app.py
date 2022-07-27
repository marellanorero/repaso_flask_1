from flask import Flask, jsonify, render_template, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db

app = Flask(__name__)
app.url_map.slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db.init_app(app)
Migrate(app, db) #db init (inicializa), db migrate (queris para base de datos), db upgrate (lleva las bases de datos)
CORS(app)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    
    return jsonify(users), 200


if __name__ == '__main__' :
    app.run()