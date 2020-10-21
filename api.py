#!/usr/bin/env python
import os
import shutil
import tempfile
import time
from sys import path

from flask import Flask, abort, request, jsonify, g, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import jwt
from sqlalchemy import engine

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
# initialization
from werkzeug.utils import secure_filename

from helper import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(32), index=True)
    prenom = db.Column(db.String(32), index=True)
    numero = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    groupeTD = db.Column(db.String(32), index=True)
    mail = db.Column(db.String(128))
    genre = db.Column(db.Integer)
    rank = db.Column(db.Integer)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'numero': self.numero,
            'groupeTD':self.groupeTD,
            'mail':self.mail,
            'genre':self.genre
        }

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])


class ForumInfo(db.Model):
    __tablename__ = 'ForumInfo'
    id_forum_info = db.Column(db.Integer, primary_key=True)
    lien_visio = db.Column(db.String(128))
    lien_video = db.Column(db.String(128))


class ParticipationForum(db.Model):
    __tablename__='ParticiationForum'
    id_participation_forum_info = db.Column(db.Integer, primary_key=True)
    id_formation = db.Column(db.Integer, db.ForeignKey('Formation.id_formation'))
    id_forum_info = db.Column(db.Integer, db.ForeignKey('ForumInfo.id_forum_info'))
    annee = db.Column(db.Integer)

class TypeEcole(db.Model):
    __tablename__ = 'TypeEcole'
    id_type_ecole = db.Column(db.Integer, primary_key=True)
    nom_type = db.Column(db.String(128))


class Ecole(db.Model):
    __tablename__ = 'Ecole'
    id_ecole = db.Column(db.Integer, primary_key=True)
    nom_ecole = db.Column(db.String(128))
    id_type_ecole = db.Column(db.Integer, db.ForeignKey('TypeEcole.id_type_ecole'))
    id_adresse_ecole = db.Column(db.Integer, db.ForeignKey('Adresse.id_adresse'))


class Adresse(db.Model):
    __tablename__ = 'Adresse'
    id_adresse = db.Column(db.Integer, primary_key=True)
    num_rue = db.Column(db.String(128))
    nom_rue = db.Column(db.String(128))
    ville = db.Column(db.String(128))
    cp = db.Column(db.String(128))
    pays = db.Column(db.String(128))


class ResponsableFormation(db.Model):
    __tablename__ = 'ResponsableFormation'
    id_responsable = db.Column(db.Integer, primary_key=True)
    nom_responsable = db.Column(db.String(128))
    mail_responsable = db.Column(db.String(128))
    telephone_responsable = db.Column(db.String(128))


class Candidature(db.Model):
    __tablename__ = 'Candidature'
    id_candidature = db.Column(db.Integer, primary_key=True)
    id_etudiant = db.Column(db.Integer, db.ForeignKey('User.id'))
    id_voeux = db.Column(db.Integer, db.ForeignKey('Voeux.id_voeux'))
    date_candidature = db.Column(db.Integer)
    deadline_dossier = db.Column(db.Integer)
    validationPE = db.Column(db.Boolean)
    id_formation = db.Column(db.Integer, db.ForeignKey('Formation.id_formation'))


class Formation(db.Model):
    __tablename__ = 'Formation'
    id_formation = db.Column(db.Integer, primary_key=True)
    specialite = db.Column(db.String(128))
    description = db.Column(db.String(255))
    site_web_url = db.Column(db.String(255))
    brochure_url = db.Column(db.String(255))
    alternance = db.Column(db.Boolean)
    type_formation = db.Column(db.Boolean)
    id_responsable = db.Column(db.Integer, db.ForeignKey('ResponsableFormation.id_responsable'))
    id_ecole = db.Column(db.Integer, db.ForeignKey('Ecole.id_ecole'))


class ProfilRecruter(db.Model):
    __tablename__ = 'ProfilRecruter'
    id_profil_recruter = db.Column(db.Integer, primary_key=True)
    id_formation = db.Column(db.Integer, db.ForeignKey('Formation.id_formation'))
    id_profil = db.Column(db.Integer, db.ForeignKey('Profil.id_profil'))


class Profil(db.Model):
    __tablename__ = 'Profil'
    id_profil = db.Column(db.Integer, primary_key=True)
    nom_profil = db.Column(db.String(128))


class Voeux(db.Model):
    __tablename__ = 'Voeux'
    id_voeux = db.Column(db.Integer, primary_key=True)
    ordre = db.Column(db.Integer)
    id_user = db.Column(db.Integer, db.ForeignKey('User.id'))
    id_candidature = db.Column(db.Integer, db.ForeignKey('Candidature.id_candidature'))


class actionPE(db.Model):
    __tablename__ = 'actionPE'
    id_action = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    etudiant = db.Column(db.Integer, db.ForeignKey('User.id'))
    id_candidature = db.Column(db.Integer, db.ForeignKey('Candidature.id_candidature'))




@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# ----------------------------ADMIN
# Check
@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


# ----------------------------USER
@app.route('/api/user/registratoin', methods=['POST'])
@auth.login_required
def user_registration():


    nom = request.json.get('nom')
    prenom = request.json.get('prenom')
    numero = request.json.get('numero')
    password = request.json.get('password')
    groupeTD = request.json.get('groupeTD')
    mail = request.json.get('mail')
    genre = request.json.get('genre')
    rank = Rank.USER.value

    if nom is None or password is None or mail is None:
        abort(400)  # missing arguments
    if User.query.filter_by(nom=nom).first() is not None:
        print("existing")
        abort(400)  # existing user
    if g.user.rank != Rank.ADMIN.value:
        abort(403)
    user = User(nom=nom)
    user.hash_password(password)
    user.prenom = prenom
    user.numero = numero
    user.groupeTD = groupeTD
    user.mail = mail
    user.genre = genre
    user.rank = rank
    db.session.add(user)
    db.session.commit()

    return (jsonify({'nom': user.nom}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/api/users/', methods=['GET'])
@auth.login_required
def get_users():
    users = User.query.order_by(User.nom).all()
    data = []
    for u in users:
        data.append(u.serialize())
    if not users:
        return jsonify({})
    print(g.user.serialize())
    if g.user.rank != Rank.ADMIN.value:
        abort(403)
    return jsonify(data)


@app.route('/api/user/<int:id>', methods=['GET'])
@auth.login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.id != id:
        abort(403)
    return jsonify(user.serialize())


@app.route('/api/user/<int:id>', methods=['POST'])
@auth.login_required
def update_user(id):
    nom = request.json.get('nom')
    prenom = request.json.get('prenom')
    numero = request.json.get('numero')
    password = request.json.get('password')
    groupeTD = request.json.get('groupeTD')
    mail = request.json.get('mail')
    genre = request.json.get('genre')
    rank = Rank.USER.value

    if nom is None or password is None or mail is None:
        abort(400)  # missing arguments
    if User.query.filter_by(nom=nom).first() is None:
        print("not existing")
        abort(400)  # existing user
    if g.user.rank != Rank.ADMIN.value and g.user.id != id:
        abort(403)

    user = User.query.get(id)
    user.hash_password(password)
    user.nom = nom
    user.prenom = prenom
    user.numero = numero
    user.groupeTD = groupeTD
    user.mail = mail
    user.genre = genre
    user.rank = rank
    db.session.commit()


# ----------------------------ForumInfo
@app.route('/api/forum/registratoin', methods=['POST'])
@auth.login_required
def forum_registration():
    pass


@app.route('/api/forum/', methods=['GET'])
@auth.login_required
def get_forums():
    pass


@app.route('/api/forum/<int:id>', methods=['GET'])
@auth.login_required
def get_forum(id):
    pass


@app.route('/api/forum/<int:id>', methods=['POST'])
@auth.login_required
def update_forum(id):
    pass


# ----------------------------TypeEcole
@app.route('/api/typeecole/registratoin', methods=['POST'])
@auth.login_required
def typeecole_registration():
    pass


@app.route('/api/typeecole/', methods=['GET'])
@auth.login_required
def get_typeecoles():
    pass


@app.route('/api/typeecole/<int:id>', methods=['GET'])
@auth.login_required
def get_typeecole(id):
    pass


@app.route('/api/typeecole/<int:id>', methods=['POST'])
@auth.login_required
def update_typeecole(id):
    pass


# ----------------------------Ecole
@app.route('/api/typeecole/registratoin', methods=['POST'])
@auth.login_required
def ecole_registration():
    pass


@app.route('/api/ecoles/', methods=['GET'])
@auth.login_required
def get_ecoles():
    pass


@app.route('/api/ecole/<int:id>', methods=['GET'])
@auth.login_required
def get_ecole(id):
    pass


@app.route('/api/ecole/<int:id>', methods=['POST'])
@auth.login_required
def update_ecole(id):
    pass


# ----------------------------ADRESSE
@app.route('/api/adresse/registratoin', methods=['POST'])
@auth.login_required
def adresse_registration():
    pass


@app.route('/api/adresses/', methods=['GET'])
@auth.login_required
def get_adresses():
    pass


@app.route('/api/adresse/<int:id>', methods=['GET'])
@auth.login_required
def get_adresse(id):
    pass


@app.route('/api/adresse/<int:id>', methods=['POST'])
@auth.login_required
def update_adresse(id):
    pass


# ----------------------------RESPONSABLE
@app.route('/api/responsable/registratoin', methods=['POST'])
@auth.login_required
def responsable_registration():
    pass


@app.route('/api/responsable/', methods=['GET'])
@auth.login_required
def get_responsables():
    pass


@app.route('/api/responsable/<int:id>', methods=['GET'])
@auth.login_required
def get_responsable(id):
    pass


@app.route('/api/responsable/<int:id>', methods=['POST'])
@auth.login_required
def update_responsable(id):
    pass


# ----------------------------CANDIDATURE
@app.route('/api/candidature/registratoin', methods=['POST'])
@auth.login_required
def candidature_registration():
    pass


@app.route('/api/candidature/', methods=['GET'])
@auth.login_required
def get_candidatures():
    pass


@app.route('/api/candidature/<int:id>', methods=['GET'])
@auth.login_required
def get_candidature(id):
    pass


@app.route('/api/candidature/<int:id>', methods=['POST'])
@auth.login_required
def update_candidature(id):
    pass


# ----------------------------FORMATION
@app.route('/api/formation/registratoin', methods=['POST'])
@auth.login_required
def formation_registration():
    pass


@app.route('/api/formation/', methods=['GET'])
@auth.login_required
def get_formations():
    pass


@app.route('/api/formation/<int:id>', methods=['GET'])
@auth.login_required
def get_formation(id):
    pass


@app.route('/api/formation/<int:id>', methods=['POST'])
@auth.login_required
def update_formation(id):
    pass


# ----------------------------PROFILRECRUTE
@app.route('/api/profilerecrute/registratoin', methods=['POST'])
@auth.login_required
def profilerecrute_registration():
    pass


@app.route('/api/profilrecrute/', methods=['GET'])
@auth.login_required
def get_profilrecrutes():
    pass


@app.route('/api/profilrecrute/<int:id>', methods=['GET'])
@auth.login_required
def get_profilrecrute(id):
    pass


@app.route('/api/profilrecrute/<int:id>', methods=['POST'])
@auth.login_required
def update_profilrecrute(id):
    pass


# ----------------------------PROFIL
@app.route('/api/profil/registratoin', methods=['POST'])
@auth.login_required
def profil_registration():
    pass


@app.route('/api/profil/', methods=['GET'])
@auth.login_required
def get_profils():
    pass


@app.route('/api/profil/<int:id>', methods=['GET'])
@auth.login_required
def get_profil(id):
    pass


@app.route('/api/profil/<int:id>', methods=['POST'])
@auth.login_required
def update_profil(id):
    pass


# ----------------------------VOEUX
@app.route('/api/voeux/registratoin', methods=['POST'])
@auth.login_required
def voeux_registration():
    pass


@app.route('/api/allvoeux/', methods=['GET'])
@auth.login_required
def get_voeuxs():
    pass


@app.route('/api/voeux/<int:id>', methods=['GET'])
@auth.login_required
def get_voeux(id):
    pass


@app.route('/api/voeux/<int:id>', methods=['POST'])
@auth.login_required
def update_voeux(id):
    pass

# ----------------------------ACTIONPE
@app.route('/api/actionpe/registratoin', methods=['POST'])
@auth.login_required
def actionpe_registration():
    pass


@app.route('/api/actionpes/', methods=['GET'])
@auth.login_required
def get_actionpes():
    pass


@app.route('/api/actionpe/<int:id>', methods=['GET'])
@auth.login_required
def get_actionpe(id):
    pass


@app.route('/api/actionpe/<int:id>', methods=['POST'])
@auth.login_required
def update_actionpe(id):
    pass

@app.route('/')
def get_api_endpoint():
    return jsonify(api_endpoint())


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.nom})


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()

    app.run(debug=True)
