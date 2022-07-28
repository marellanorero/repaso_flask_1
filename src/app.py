
from flask import Flask, jsonify, render_template, jsonify, request
from pkg_resources import require
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Profile, Contact

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
    users = list(map(lambda user: user.serialize_with_profile(), users))

    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def post_users():
    name=request.json.get('name')
    lastname=request.json.get('lastname')
    email=request.json.get('email')
    password=request.json.get('password')

    bio=request.json.get('bio', "")
    twitter=request.json.get('twitter', "")
    facebook=request.json.get('facebook', "")
    instagram=request.json.get('instagram', "")
    linkedin=request.json.get('linkedin', "")

    if not email: return jsonify({ "status": False, "msg": "email is required" }), 400

    user = User.query.filter_by(email=email).first()
    if user: return jsonify({ "status": False, "msg": "Email already in use!" }), 400

    """
    user=User()
    user.name=name
    user.lastname=lastname
    user.email=email
    user.password=password
    user.save()

    profile=Profile()
    profile.bio=bio
    profile.twitter=twitter
    profile.facebook=facebook
    profile.instagram=instagram
    profile.linkedin=linkedin
    profile.user_id=user.id
    profile.save()
    """
    user=User()
    user.name=name
    user.lastname=lastname
    user.email=email
    user.password=password
  
    profile=Profile()
    profile.bio=bio
    profile.twitter=twitter
    profile.facebook=facebook
    profile.instagram=instagram
    profile.linkedin=linkedin

    user.profile = profile
    user.save()


    return jsonify(user.serialize_with_profile()), 201

@app.route('/api/users/<int:id>', methods=['PUT'])
def put_users(id):
    name=request.json.get('name')
    lastname=request.json.get('lastname')
    email=request.json.get('email')
    password=request.json.get('password')

    bio=request.json.get('bio', "")
    twitter=request.json.get('twitter', "")
    facebook=request.json.get('facebook', "")
    instagram=request.json.get('instagram', "")
    linkedin=request.json.get('linkedin', "")

    """
    user = User.query.get(id)
    user.name = name
    user.lastname = lastname
    user.email = email
    user.password = password
    user.update()

    profile=Profile.query.filter_by(user_id=user.id).first()
    profile.bio=bio
    profile.twitter=twitter
    profile.facebook=facebook
    profile.instagram=instagram
    profile.linkedin=linkedin
    profile.update()
    """

    user = User.query.get(id)
    user.name = name
    user.lastname = lastname
    user.email = email
    user.password = password
    user.profile.bio=bio
    user.profile.twitter=twitter
    user.profile.facebook=facebook
    user.profile.instagram=instagram
    user.profile.linkedin=linkedin
    user.update()




    return jsonify(user.serialize_with_profile()), 200

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):

    user=User.query.get(id)

    if not user: return jsonify({"status":False, "msg": "User doesn't exist"}), 404

    user.delete()

    return jsonify({ "status": True, "msg": "User deleted!"}), 200

@app.route('/api/user/<int:user_id>/contacts', methods=['GET', 'POST'])
@app.route('/api/user/<int:user_id>/contacts/<int:contact_id>', methods=['GET', 'PUT', 'DELETE'])
def contact_by_user(user_id, contact_id=None):
    if request.method == 'GET':

        if contact_id is not None:
            contact = Contact.query.filter_by(user_id=user_id, id=contact_id).first()
            if not contact: return jsonify({"status": False, "msg": "Contact not found"}), 404
            return jsonify(contact.serialize()), 200
        else:
            contacts = Contact.query.filter_by(user_id=user_id)
            contacts= list(map(lambda contact: contact.serialize(), contacts))
            return jsonify(contacts), 200
    if request.method == 'POST':
        name=request.json.get("name")
        phone_work= request.json.get("phone_work")
        phone_home=request.json.get("phone_home", "")
        email=request.json.get("email", "")

        contact = Contact()
        contact.name=name
        contact.phone_work=phone_work
        contact.phone_home=phone_home
        contact.email=email
        contact.user_id=user_id
        contact.save()

        return jsonify(contact.serialize()), 201
    
    if request.method == 'PUT':

        name=request.json.get("name")
        phone_work= request.json.get("phone_work")
        phone_home=request.json.get("phone_home", "")
        email=request.json.get("email", "")

        contact = Contact.query.filter_by(user_id=user_id, id=contact_id).first()
        if not contact: return jsonify({"status": False, "msg": "Contact not found"}), 404

        contact = Contact()
        contact.name=name
        contact.phone_work=phone_work
        contact.phone_home=phone_home
        contact.email=email
        contact.update()

        return jsonify(contact.serialize()), 201


if __name__ == '__main__' :
    app.run()