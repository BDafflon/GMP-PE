#!/usr/bin/env python
import os
import shutil
import tempfile
import time
from sys import path

from flask import Flask, abort, request, jsonify, g, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import jwt
from flask_cors import CORS, cross_origin
from sqlalchemy import engine, desc, true

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
# initialization
from werkzeug.utils import secure_filename

from helper import *

from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, origins="*", allow_headers="*")
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class Modification(db.Model):
    __tablename__ ="Modification"
    id_modification = db.Column(db.Integer, primary_key=True)
    type_modification= db.Column(db.Integer)
    message = db.Column(db.String(255))
    id_reference =  db.Column(db.Integer)

class AvisProf(db.Model):
    __tablename__ = 'AvisProf'
    id_avis = db.Column(db.Integer, primary_key=True)
    prof = db.Column(db.String(128))
    avis = db.Column(db.String(255))
    matiere = db.Column(db.String(128))
    id_candidature = db.Column(db.Integer, db.ForeignKey('Candidature.id_candidature'))

    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id_avis':self.id_avis,
            'prof':self.prof,
            'avis': self.avis,
            'id_candidature':self.id_candidature,
            'matiere':self.matiere

        }

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

    def generate_auth_token(self, expires_in=60000):
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
            'groupeTD': self.groupeTD,
            'mail': self.mail,
            'genre': self.genre,
            'rank': self.rank
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

    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id_forum_info': self.id_forum_info,
            'lien_visio': self.lien_visio,
            'lien_video': self.lien_video

        }


class ParticipationForum(db.Model):
    __tablename__ = 'ParticiationForum'
    id_participation_forum_info = db.Column(db.Integer, primary_key=True)
    id_formation = db.Column(db.Integer, db.ForeignKey('Formation.id_formation'))
    id_forum_info = db.Column(db.Integer, db.ForeignKey('ForumInfo.id_forum_info'))
    annee = db.Column(db.Integer)

    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id_participation_forum_info': self.id_participation_forum_info,
            'id_formation': self.id_formation,
            'id_forum_info': self.id_forum_info,
            'anne': self.annee
        }


class TypeEcole(db.Model):
    __tablename__ = 'TypeEcole'
    id_type_ecole = db.Column(db.Integer, primary_key=True)
    nom_type = db.Column(db.String(128))

    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id_type_ecole': 1,
            'nom_type': self.nom_type
        }


class Ecole(db.Model):
    __tablename__ = 'Ecole'
    id_ecole = db.Column(db.Integer, primary_key=True)
    nom_ecole = db.Column(db.String(128))
    complement_ecole = db.Column(db.String(128))
    description = db.Column(db.String(255))
    id_type_ecole = db.Column(db.Integer, db.ForeignKey('TypeEcole.id_type_ecole'))
    id_adresse_ecole = db.Column(db.Integer, db.ForeignKey('Adresse.id_adresse'))
    valide = db.Column(db.Boolean)

    def serialize(self):
        return {
            'id_ecole': self.id_ecole,
            'nom_ecole': self.nom_ecole,
            'complement_ecole': self.complement_ecole,
            'id_type_ecole': get_type_local(self.id_type_ecole),
            'adresse': get_adresse_local(self.id_adresse_ecole),
            'description': self.description,
            'formation': get_formation_by_ecole(self.id_ecole)
        }


def get_formation_by_ecole(id):
    formations = Formation.query.filter_by(id_ecole=id).all()
    if formations is None:
        return {}
    data = []
    for f in formations:
        data.append(f.serialize())
    return data


def get_type_local(id):
    type = TypeEcole.query.filter_by(id_type_ecole=id).first()
    if type is None:
        return 'none'
    print('----------------',id)
    return type.nom_type


def get_adresse_local(id):
    adresse = Adresse.query.filter_by(id_adresse=id).first()

    if adresse is None:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        return jsonify({})
    return adresse.serialize()


class Adresse(db.Model):
    __tablename__ = 'Adresse'
    id_adresse = db.Column(db.Integer, primary_key=True)
    num_rue = db.Column(db.String(128))
    nom_rue = db.Column(db.String(128))
    ville = db.Column(db.String(128))
    cp = db.Column(db.String(128))
    pays = db.Column(db.String(128))

    def serialize(self):
        return {
            'id_adresse': self.id_adresse,
            'num_rue': self.num_rue,
            'nom_rue': self.nom_rue,
            'ville': self.ville,
            'cp': self.cp,
            'pays': self.pays
        }


class ResponsableFormation(db.Model):
    __tablename__ = 'ResponsableFormation'
    id_responsable = db.Column(db.Integer, primary_key=True)
    nom_responsable = db.Column(db.String(128))
    prenom_responsable = db.Column(db.String(128))
    mail_responsable = db.Column(db.String(128))
    telephone_responsable = db.Column(db.String(128))
    valide = db.Column(db.Boolean)

    def serialize(self):
        return {
            'id_responsable': self.id_responsable,
            'nom_responsable': self.nom_responsable,
            'prenom_responsable': self.prenom_responsable,
            'mail_responsable': self.mail_responsable,
            'telephone_responsable': self.telephone_responsable
        }


class Candidature(db.Model):
    __tablename__ = 'Candidature'
    id_candidature = db.Column(db.Integer, primary_key=True)
    id_etudiant = db.Column(db.Integer, db.ForeignKey('User.id'))
    etat = db.Column(db.Integer)
    date_candidature = db.Column(db.Integer)
    deadline_dossier = db.Column(db.Integer)
    validationPE = db.Column(db.Boolean)
    voeux = db.Column(db.Integer)
    id_formation = db.Column(db.Integer, db.ForeignKey('Formation.id_formation'))

    def serialize(self):
        return {
            'id_candidature': self.id_candidature,
            'id_etudiant': self.id_etudiant,
            'etat': self.etat,
            'date_candidature': self.date_candidature,
            'deadline_dossier': self.deadline_dossier,
            'validationPE': self.validationPE,
            'id_formation': self.id_formation,
            'voeux': self.voeux,
            'formation-c':[]
        }


class Formation(db.Model):
    __tablename__ = 'Formation'
    id_formation = db.Column(db.Integer, primary_key=True)
    specialite = db.Column(db.String(128))
    description = db.Column(db.String(255))
    site_web_url = db.Column(db.String(255))
    brochure_url = db.Column(db.String(255))
    alternance = db.Column(db.Boolean)
    niveau = db.Column(db.Integer)
    type_formation = db.Column(db.Boolean)
    id_responsable = db.Column(db.Integer, db.ForeignKey('ResponsableFormation.id_responsable'))
    id_ecole = db.Column(db.Integer, db.ForeignKey('Ecole.id_ecole'))
    valide = db.Column(db.Boolean)

    def serialize(self):
        return {
            'id_formation': self.id_formation,
            'specialite': self.specialite,
            'description': self.description,
            'site_web_url': self.site_web_url,
            'brochure_url': self.brochure_url,
            'alternance': self.alternance,
            'type_formation': self.type_formation,
            'id_ecole': self.id_ecole,
            'niveau':self.niveau,
            'id_responsable': self.id_responsable,
            'ecole-f':[]
        }


class ProfilRecruter(db.Model):
    __tablename__ = 'ProfilRecruter'
    id_profil_recruter = db.Column(db.Integer, primary_key=True)
    id_formation = db.Column(db.Integer, db.ForeignKey('Formation.id_formation'))
    id_profil = db.Column(db.Integer, db.ForeignKey('Profil.id_profil'))

    def serialize(self):
        return {
            'id_profil_recruter': self.id_profil_recruter,
            'id_formation': self.id_formation,
            'id_profil': self.id_profil
        }


class Profil(db.Model):
    __tablename__ = 'Profil'
    id_profil = db.Column(db.Integer, primary_key=True)
    nom_profil = db.Column(db.String(128))

    def serialize(self):
        return {
            'id_profil': self.id_profil,
            'nom_profil': self.nom_profil
        }


class actionPE(db.Model):
    __tablename__ = 'actionPE'
    id_action = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    id_etudiant = db.Column(db.Integer, db.ForeignKey('User.id'))
    id_candidature = db.Column(db.Integer, db.ForeignKey('Candidature.id_candidature'))
    lu = db.Column(db.Boolean)

    def serialize(self):
        return {
            'id_action': self.id_action,
            'action': self.action,
            'id_etudiant': self.id_etudiant,
            'id_candidature': self.id_candidature
        }


# Check
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    print("user or tocken " + username_or_token)
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(mail=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


# ----------------------------ADMIN
# Check
@app.route('/api/token', methods=['GET', 'POST'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    response = jsonify({'user': g.user.serialize(), 'token': 'token', 'duration': 600})
    return response


# ----------------------------avis
# Check
@app.route('/api/avis/registration', methods=['POST'])
@auth.login_required
def avis_registration():
    prof = request.json.get('prof')
    avis = request.json.get('avis')
    matiere = request.json.get('matiere')
    id_candidature = request.json.get('id_candidature')


    if prof is None or avis is None or id_candidature is None:
        abort(make_response(jsonify(errors='missing parameters'), 400))
    if Candidature.query.filter_by(id_candidature=id_candidature).first() is None:
        print("existing")
        abort(make_response(jsonify(errors='User already existing'), 400))

    if g.user.rank != Rank.ADMIN.value:
        abort(make_response(jsonify(errors='Forbiden, ondy admin can add new user'), 403))

    AvisP = AvisProf(prof=prof)
    AvisP.id_candidature=id_candidature
    AvisP.avis=avis
    AvisP.matiere = matiere
    db.session.add(AvisP)
    db.session.commit()

    return jsonify(AvisP.serialize())


# Check
@app.route('/api/avis/', methods=['GET'])
@auth.login_required
def get_avis():
    avis = AvisProf.query.order_by(AvisProf.id_candidature).all()
    data = []
    for u in avis:
        data.append(u.serialize())

    if g.user.rank != Rank.ADMIN.value or g.user.rank != Rank.USER.value:
        abort(make_response(jsonify(errors='Forbiden, ondy admin can use endpoint'), 403))

    return jsonify(data)


# Check
@app.route('/api/avis/<int:id>', methods=['GET'])
@auth.login_required
def get_avis_by_candidature(id):
    avis = AvisProf.query.filter_by(id_candidature=id).all()
    if not avis:
        abort(make_response(jsonify(errors='No avis ' + str(id)), 404))

    if g.user.rank != Rank.ADMIN.value and g.user.id != id:
        abort(make_response(jsonify(errors='Forbiden, ondy user can use endpoint'), 403))

    data = []
    for u in avis:
        data.append(u.serialize())
    return jsonify(data)


# Check
@app.route('/api/user/<int:id>', methods=['POST'])
@auth.login_required
def update_avis(id):

    prof = request.json.get('prof')
    avis = request.json.get('avis')
    id_candidature = request.json.get('id_candidature')

    if prof is None or avis is None or id_candidature is None:
        abort(make_response(jsonify(errors='Missing parameters'), 400))
    avis = AvisProf.query.filter_by(id_avis=id).first()
    if avis is None:
        abort(make_response(jsonify(errors='Avis not found'), 400))

    if g.user.rank != Rank.ADMIN.value and g.user.id != id:
        abort(make_response(jsonify(errors='Forbiden, ondy user can use endpoint'), 403))

    avis.prof = prof
    avis.id_candidature = id_candidature
    avis.avis = avis

    db.session.commit()
    return jsonify(avis.serialize())


# ----------------------------USER
# Check
@app.route('/api/user/registration', methods=['POST'])
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
        abort(make_response(jsonify(errors='missing parameters'), 400))
    if User.query.filter_by(mail=mail).first() is not None:
        print("existing")
        abort(make_response(jsonify(errors='User already existing'), 400))

    if g.user.rank != Rank.ADMIN.value:
        abort(make_response(jsonify(errors='Forbiden, ondy admin can add new user'), 403))

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

@app.route("/api/user/all", methods=["DELETE"])
@auth.login_required
def users_delete():
    print("del user")
    if g.user.rank != Rank.ADMIN.value :
        abort(403)
    user = User.query.filter(User.rank== 2).all()
    for f in user:
        candidatures = Candidature.query.filter(Candidature.id_etudiant==f.id).all()
        ape = actionPE.query.filter(actionPE.id_etudiant==f.id).all()
        for ap in ape:
            db.session.delete(ap)
        for c in candidatures:
            avis = AvisProf.query.filter(AvisProf.id_candidature==c.id_candidature).all()
            for a in avis:
                db.session.delete(a)
            db.session.delete(c)

        db.session.delete(f)
    db.session.commit()
    return jsonify({'message':'done'})

@app.route('/api/userd/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_user(id):
    record_obj = db.session.query(User).filter(User.id == id).first()
    if record_obj is not None:
        if g.user.rank == Rank.ADMIN.value:
            db.session.delete(record_obj)
            db.session.commit()
            return jsonify({"message": "OK"})
        else:
            abort(make_response(jsonify(errors='Forbiden'), 403))

    abort(make_response(jsonify(errors='no candidature found'), 403))

# Check
@app.route('/api/users/', methods=['GET'])
@auth.login_required
def get_users():
    users = User.query.order_by(User.nom).all()
    data = []
    for u in users:
        can = Candidature.query.filter_by(id_etudiant=u.id).all()
        d=[]
        us = u.serialize()
        for c in can:
            d.append(c.serialize())
        us["candidatures"]=d
        print("uers :")
        print(us)
        data.append(us)

    if not users:
        return jsonify({})
    print(g.user.serialize())

    if g.user.rank != Rank.ADMIN.value:
        abort(make_response(jsonify(errors='Forbiden, ondy admin can use endpoint'), 403))

    return jsonify(data)


# Check
@app.route('/api/user/<int:id>', methods=['GET'])
@auth.login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(make_response(jsonify(errors='No user ' + str(id)), 404))
    if g.user.rank != Rank.ADMIN.value and g.user.id != id:
        abort(make_response(jsonify(errors='Forbiden, ondy user can use endpoint'), 403))
    return jsonify(user.serialize())


# Check
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
        abort(make_response(jsonify(errors='Missing parameters'), 400))
    if User.query.filter_by(id=id).first() is None:
        abort(make_response(jsonify(errors='User not found'), 400))
    if g.user.rank != Rank.ADMIN.value and g.user.id != id:
        abort(make_response(jsonify(errors='Forbiden, ondy user can use endpoint'), 403))

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
    return jsonify(user.serialize())


# ----------------------------ForumInfo
# Check
@app.route('/api/foruminfo/registration', methods=['POST'])
@auth.login_required
def foruminfo_registration():
    lien_visio = request.json.get('lien_visio')
    lien_video = request.json.get('lien_video')

    if lien_visio is None or lien_video is None:
        abort(make_response(jsonify(errors='Missing parameters'), 400))

    if g.user.rank != Rank.ADMIN.value:
        abort(make_response(jsonify(errors='Forbiden, ondy admin can use endpoint'), 403))

    info = ForumInfo(lien_visio=lien_visio)
    info.lien_video = lien_video
    db.session.add(info)
    db.session.commit()
    return jsonify(info.serialize())


# Check
@app.route('/api/foruminfo/', methods=['GET'])
@auth.login_required
def get_foruminfos():
    info = ForumInfo.query.order_by(ForumInfo.id_forum_info).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        abort(make_response(jsonify(errors='Info not found'), 400))

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(make_response(jsonify(errors='Forbiden, ondy user can use endpoint'), 403))

    return jsonify(data)


# Check
@app.route('/api/foruminfo/<int:id>', methods=['GET'])
@auth.login_required
def get_foruminfo(id):
    info = ForumInfo.query.filter_by(id_forum_info=id).first()

    if not info:
        abort(make_response(jsonify(errors='Info not found'), 400))

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(make_response(jsonify(errors='Forbiden, ondy user can use endpoint'), 403))
    return jsonify(info.serialize())


# Check
@app.route('/api/foruminfo/<int:id>', methods=['POST'])
@auth.login_required
def update_forum(id):
    lien_visio = request.json.get('lien_visio')
    lien_video = request.json.get('lien_video')

    if lien_visio is None or lien_video is None:
        abort(make_response(jsonify(errors='Missing parameters'), 400))

    if g.user.rank != Rank.ADMIN.value:
        abort(make_response(jsonify(errors='Forbiden, ondy admin can use endpoint'), 403))

    info = ForumInfo.query.filter_by(id_forum_info=id).first()
    if not info:
        abort(make_response(jsonify(errors='Forum info not found'), 400))
    info.lien_visio = lien_visio
    info.lien_video = lien_video
    db.session.commit()
    return jsonify(info.serialize())


# -----------------------------ParticipationForum
@app.route('/api/participationforum/registration', methods=['POST'])
@auth.login_required
def participationforum_registration():
    id_formation = request.json.get('id_formation')
    id_forum_info = request.json.get('id_forum_info')
    annee = request.json.get('annee')

    if id_formation is None or id_forum_info is None or annee is None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    info = ParticipationForum(id_formation=id_formation)
    info.id_forum_info = id_forum_info
    info.annee = int(annee)
    db.session.add(info)
    db.session.commit()
    return jsonify(info.serialize())


@app.route('/api/participationforum/', methods=['GET'])
@auth.login_required
def get_participationsforum():
    info = ParticipationForum.query.order_by(ParticipationForum.id_participation_forum_info).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        return jsonify({})
    print(g.user.serialize())

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/participationforum/<int:id>', methods=['GET'])
@auth.login_required
def get_participationforum(id):
    info = ParticipationForum.query.filter_by(id_participation_forum_info=id).first()

    if not info:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify(info.serialize())


@app.route('/api/participationforum/<int:id>', methods=['POST'])
@auth.login_required
def update_participationforum(id):
    id_formation = request.json.get('id_formation')
    id_forum_info = request.json.get('id_forum_info')
    annee = request.json.get('annee')

    if id_formation is None or id_forum_info is None or annee is None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    info = ForumInfo.query.filter_by(id_forum_info=id).first()
    if not info:
        abort(400)
    info.id_formation = id_formation
    info.id_forum_info = id_forum_info
    info.annee = int(annee)
    db.session.commit()
    return jsonify(info.serialize())


# ----------------------------TypeEcole
# Check
@app.route('/api/typeecole/registration', methods=['POST'])
@auth.login_required
def typeecole_registration():
    nom_type = request.json.get('nom_type')

    if nom_type is None:
        abort(make_response(jsonify(errors='Missing parameters'), 400))

    if g.user.rank != Rank.ADMIN.value:
        abort(make_response(jsonify(errors='Forbiden : only admin can use endpoint'), 403))

    type = TypeEcole(nom_type=nom_type)

    db.session.add(type)
    db.session.commit()
    return jsonify(type.serialize())


@app.route('/api/typeecole/', methods=['GET'])
@auth.login_required
def get_typeecoles():
    info = TypeEcole.query.order_by(TypeEcole.nom_type).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        abort(make_response(jsonify(errors='No data'), 403))
    print(g.user.serialize())

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(make_response(jsonify(errors='Forbiden : only user can use endpoint'), 403))

    return jsonify(data)


@app.route('/api/typeecole/<int:id>', methods=['GET'])
@auth.login_required
def get_typeecole(id):
    info = TypeEcole.query.filter_by(id_type_ecole=id).first()

    if not info:
        return jsonify({})

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(info.serialize())


@app.route('/api/typeecole/<int:id>', methods=['POST'])
@auth.login_required
def update_typeecole(id):
    nom_type = request.json.get('nom_type')
    info = TypeEcole.query.filter_by(TypeEcole.id_type_ecole).first()

    if nom_type is None:
        abort(400)
    if not info:
        return jsonify({})

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    info.nom_type = nom_type
    db.session.commit()
    return jsonify(info.serialize())


# ----------------------------Ecole
@app.route('/api/ecole/registration', methods=['POST'])
@auth.login_required
def ecole_registration():
    nom_ecole = request.json.get('nom_ecole')
    id_type_ecole = request.json.get('id_type_ecole')
    complement = request.json.get('complement')
    description = request.json.get('description')
    id_adresse_ecole = request.json.get('id_adresse_ecole')

    if nom_ecole is None or id_type_ecole is None or id_adresse_ecole is None:
        abort(make_response(jsonify(errors='missing data'), 400))
    if g.user.rank != Rank.ADMIN.value:
        abort(make_response(jsonify(errors='Forbiden'), 403))

    ecole = Ecole.query.filter_by(nom_ecole=nom_ecole).first()
    adresse = Adresse.query.filter_by(id_adresse=id_adresse_ecole).first()
    type = TypeEcole.query.filter_by(id_type_ecole=id_type_ecole).first()
    if ecole is not None:
        abort(make_response(jsonify(errors='Existing'), 403))
    if adresse is None:
        abort(make_response(jsonify(errors='missing type / missing adress'), 403))

    if type is None :
        id_type_ecole=0

    ecole = Ecole(nom_ecole=nom_ecole)
    ecole.id_type_ecole = int(id_type_ecole)
    ecole.id_adresse_ecole = int(id_adresse_ecole)
    ecole.description = description
    ecole.complement_ecole = complement
    db.session.add(ecole)
    db.session.commit()
    return jsonify(ecole.serialize())


@app.route('/api/ecoles/', methods=['GET'])
@auth.login_required
def get_ecoles():
    print(g.user)
    info = Ecole.query.order_by(Ecole.nom_ecole).all()
    data = []
    for u in info:
        print(u.serialize(),'\n\n')
        data.append(u.serialize())
    if not info:
        return jsonify({})

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/ecole/<int:id>', methods=['GET'])
@auth.login_required
def get_ecole(id):
    ecole = Ecole.query.filter_by(id_ecole=id).first()

    if ecole is None:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify(ecole.serialize())


@app.route('/api/ecole/<int:id>', methods=['POST'])
@auth.login_required
def update_ecole(id):
    nom_ecole = request.json.get('nom_ecole')
    id_type_ecole = request.json.get('id_type_ecole')
    id_adresse_ecole = request.json.get('id_adresse_ecole')

    if nom_ecole is None or id_type_ecole is None or id_adresse_ecole is None:
        abort(400)
    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    ecole = Ecole.query.filter_by(id_ecole=id).first()
    adresse = Adresse.query.filter_by(id_adresse=id_adresse_ecole).first()
    type = TypeEcole.query.filter_by(id_type_ecole=id_type_ecole).first()
    if ecole is None:
        abort(400)
    if type is None or adresse is None:
        abort(400)

    ecole.id_type_ecole = int(id_type_ecole)
    ecole.id_adresse_ecole = int(id_adresse_ecole)
    ecole.nom_ecole = nom_ecole
    db.session.commit()
    return jsonify(ecole.serialize())

@app.route("/api/ecole/all", methods=["DELETE"])
@auth.login_required
def ecole_delete():
    print("del ecole")
    if g.user.rank != Rank.ADMIN.value :
        abort(403)
    ecoles = Ecole.query.order_by(Ecole.id_ecole).all()
    for e in ecoles:
        formation = Formation.query.filter(Formation.id_ecole==e.id_ecole).all()
        for f in formation :
            candidature = Candidature.query.filter(Candidature.id_formation==f.id_formation).all()
            for c in candidature:
                db.session.delete(c)
            db.session.delete(f)
        db.session.delete(e)
    db.session.commit()
    return jsonify({'message':'done'})

# ----------------------------ADRESSE
@app.route('/api/adresse/registration', methods=['POST'])
@auth.login_required
def adresse_registration():
    num_rue = request.json.get('num_rue')
    nom_rue = request.json.get('nom_rue')
    ville = request.json.get('ville')
    cp = request.json.get('cp')
    pays = request.json.get('pays')

    if num_rue is None or nom_rue is None or ville is None or cp is None or pays is None:
        abort(make_response(jsonify(errors='Missing parameters'), 400))

    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    adresse = Adresse.query.filter_by(num_rue=num_rue, nom_rue=nom_rue, ville=ville, cp=cp, pays=pays).first()
    if adresse is not None:
        return jsonify(adresse.serialize())

    adr = Adresse(num_rue=num_rue)
    adr.nom_rue = nom_rue
    adr.ville = ville
    adr.cp = cp
    adr.pays = pays
    db.session.add(adr)
    db.session.commit()
    print(adr)
    return jsonify(adr.serialize())


@app.route('/api/adresses/', methods=['GET'])
@auth.login_required
def get_adresses():
    info = Adresse.query.order_by(Adresse.ville).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        return jsonify({})

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    response = jsonify(data)

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/api/adresse/<int:id>', methods=['GET'])
@auth.login_required
def get_adresse(id):
    adresse = Adresse.query.filter_by(id_adresse=id).first()

    if adresse is None:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify(adresse.serialize())


@app.route('/api/adresse/<int:id>', methods=['POST'])
@auth.login_required
def update_adresse(id):
    num_rue = request.json.get('num_rue')
    nom_rue = request.json.get('nom_rue')
    ville = request.json.get('ville')
    cp = request.json.get('cp')
    pays = request.json.get('pays')

    if num_rue is None or nom_rue is None or ville is None or cp is None or pays is None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    adr = Adresse.query.filter_by(id_adresse=id).first()
    if adr is not None:
        abort(400)

    adr.nom_rue = nom_rue
    adr.ville = ville
    adr.cp = cp
    adr.pays = pays
    db.commit()
    return jsonify(adr.ser)


# ----------------------------RESPONSABLE
@app.route('/api/responsable/registration', methods=['POST'])
@auth.login_required
def responsable_registration():
    nom_responsable = request.json.get('nom_responsable')
    prenom_responsable = request.json.get('prenom_responsable')
    mail_responsable = request.json.get('mail_responsable')
    telephone_responsable = request.json.get('telephone_responsable')

    if nom_responsable is None or mail_responsable is None or telephone_responsable is None:
        abort(400)
    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    res = ResponsableFormation.query.filter_by(nom_responsable=nom_responsable,
                                               mail_responsable=mail_responsable).first()
    if res is not None:
        return jsonify(res.serialize())

    resp = ResponsableFormation(nom_responsable=nom_responsable)
    resp.mail_responsable = mail_responsable
    resp.telephone_responsable = telephone_responsable
    resp.prenom_responsable = prenom_responsable
    db.session.add(resp)
    db.session.commit()
    return jsonify(resp.serialize())


@app.route('/api/responsables/', methods=['GET'])
@auth.login_required
def get_responsables():
    info = ResponsableFormation.query.order_by(ResponsableFormation.id_responsable).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        return jsonify({})

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/responsable/<int:id>', methods=['GET'])
@auth.login_required
def get_responsable(id):
    resp = ResponsableFormation.query.filter_by(id_responsable=id).first()

    if resp is None:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(resp.serialize())


@app.route('/api/responsable/<int:id>', methods=['POST'])
@auth.login_required
def update_responsable(id):
    nom_responsable = request.json.get('nom_responsable')
    mail_responsable = request.json.get('mail_responsable')
    telephone_responsable = request.json.get('telephone_responsable')

    if nom_responsable is None or mail_responsable is None or telephone_responsable is None:
        abort(400)
    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    resp = ResponsableFormation.query.filter_by(id_responsable=id).first()
    if resp is None:
        abort(400)

    resp.nom_responsable = nom_responsable
    resp.mail_responsable = mail_responsable
    resp.telephone_responsable = telephone_responsable
    db.commit()
    return jsonify(resp.serialize())


# ----------------------------CANDIDATURE
@app.route('/api/candidature/registration', methods=['POST'])
@auth.login_required
def candidature_registration():
    id_etudiant = request.json.get('id_etudiant')
    date_candidature = request.json.get('date_candidature')
    deadline_dossier = request.json.get('deadline_dossier')
    validationPE = request.json.get('validationPE')
    id_formation = request.json.get('id_formation')

    if id_etudiant is None or id_formation is None:
        abort(make_response(jsonify(errors='Missing parameters'), 400))

    etu = User.query.filter_by(id=id_etudiant).first()
    formation = Formation.query.filter_by(id_formation=id_formation).first()

    if etu is None or formation is None:
        abort(make_response(jsonify(errors='Formation or etu not found'), 400))

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(make_response(jsonify(errors='Forbiden'), 403))

    ex = Candidature.query.filter_by(id_etudiant=id_etudiant, id_formation=id_formation).first()
    if ex is not None:
        return jsonify(ex.serialize())
    nbVoeux = Candidature.query.filter_by(id_etudiant=id_etudiant).count()

    candidature = Candidature(id_etudiant=id_etudiant)
    candidature.voeux = nbVoeux + 1
    candidature.date_candidature = date_candidature
    candidature.deadline_dossier = deadline_dossier
    candidature.validationPE = validationPE
    candidature.id_formation = id_formation
    db.session.add(candidature)
    db.session.commit()
    return jsonify(candidature.serialize())


@app.route('/api/candidatures/', methods=['GET'])
@auth.login_required
def get_candidatures():
    info = Candidature.query.order_by(Candidature.id_etudiant).all()
    data = []
    for u in info:
        etu = User.query.filter(User.id==u.id_etudiant).first()
        d = u.serialize()
        d["etudiant"]=etu.serialize()
        acpe = actionPE.query.filter(actionPE.id_candidature == u.id_candidature, actionPE.lu == False).all()
        d["nbAction"] = len(acpe)
        formation = Formation.query.filter(Formation.id_formation==u.id_formation).first()
        ecole = Ecole.query.filter(Ecole.id_ecole==formation.id_ecole).first()
        fs = formation.serialize()
        fs["ecole"]=ecole.serialize()

        d["formation"] = fs
        data.append(d)
    if not info:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/candidature/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_candidatures(id):
    record_obj = db.session.query(Candidature).filter(Candidature.id_candidature == id).first()
    if record_obj is not None:
        if record_obj.id_etudiant == g.user.id or g.user.rank != Rank.ADMIN.value:
            db.session.delete(record_obj)
            db.session.commit()
            return jsonify({"message": "OK"})
        else:
            abort(make_response(jsonify(errors='Forbiden'), 403))

    abort(make_response(jsonify(errors='no candidature found'), 403))


@app.route('/api/candidature/up/<int:id>', methods=['GET'])
@auth.login_required
def up_candidatures(id):
    can = Candidature.query.filter_by(id_candidature=id).first()

    if can is not None:
        if can.voeux != 1:
            can2 = Candidature.query.filter_by(id_etudiant=g.user.id, voeux=can.voeux - 1).first()
            if can2 is not None:
                old = can.voeux
                can.voeux = old - 1
                can2.voeux = old
                db.session.commit()
                return jsonify({"message": "OK"})
            else:
                abort(make_response(jsonify(errors='swao error'), 403))
        else:
            abort(make_response(jsonify(errors='voeux is the fist'), 403))
    else:
        abort(make_response(jsonify(errors='no candidature found'), 403))

    abort(make_response(jsonify(errors='no candidature found'), 403))


@app.route('/api/candidature/down/<int:id>', methods=['GET'])
@auth.login_required
def down_candidatures(id):
    can = Candidature.query.filter_by(id_candidature=id).first()
    max = Candidature.query.filter_by(id_etudiant=g.user.id).order_by(desc(Candidature.voeux)).first().voeux
    print(max)
    if can is not None:
        if can.voeux != max:
            can2 = Candidature.query.filter_by(id_etudiant=g.user.id, voeux=can.voeux + 1).first()
            if can2 is not None:
                old = can.voeux
                can.voeux = old + 1
                can2.voeux = old
                db.session.commit()
                return jsonify({"message": "OK"})
            else:
                abort(make_response(jsonify(errors='swap error'), 403))
        else:
            abort(make_response(jsonify(errors='voeux is the last'), 403))
    else:
        abort(make_response(jsonify(errors='no candidature found'), 403))

    abort(make_response(jsonify(errors='no candidature found'), 403))


@app.route('/api/candidatures_user/<int:id>', methods=['GET'])
@auth.login_required
def get_candidatures_user(id):
    info = Candidature.query.filter(Candidature.id_etudiant==id).all()
    data = []
    for u in info:
        etu = User.query.filter(User.id == u.id_etudiant).first()
        d = u.serialize()
        acpe= actionPE.query.filter(actionPE.id_candidature==u.id_candidature,actionPE.lu==False).all()
        d["nbAction"]= len(acpe)
        d["etudiant"] = etu.serialize()

        formation = Formation.query.filter(Formation.id_formation == u.id_formation).first()
        ecole = Ecole.query.filter(Ecole.id_ecole == formation.id_ecole).first()
        fs = formation.serialize()
        fs["ecole"] = ecole.serialize()

        d["formation"] = fs
        data.append(d)
    if not info:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/candidature/<int:id>', methods=['GET'])
@auth.login_required
def get_candidature(id):
    can = Candidature.query.filter_by(id_candidature=id).first()

    if can is None:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify(can.serialize())


@app.route('/api/candidature/<int:id>', methods=['POST'])
@auth.login_required
def update_candidature(id):
    id_etudiant = request.json.get('id_etudiant')
    date_candidature = request.json.get('date_candidature')
    deadline_dossier = request.json.get('deadline_dossier')
    validationPE = request.json.get('validationPE')
    id_formation = request.json.get('id_formation')
    nbVoeux = request.json.get('nbVoeux')
    print(id_etudiant,date_candidature,deadline_dossier,id_formation)
    if id_etudiant is None is None or date_candidature is None or deadline_dossier is None or id_formation is None:
        abort(make_response(jsonify(errors='missing parameters'), 400))

    etu = User.query.filter_by(id=id_etudiant).first()
    formation = Formation.query.filter_by(id_formation=id_formation).first()
    if etu is None or formation is None:
        abort(make_response(jsonify(errors='missing etu/for'), 400))

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(make_response(jsonify(errors='Forbiden'), 400))

    candidature = Candidature.query.filter_by(id_candidature=id).first()
    if candidature is None:
        abort(make_response(jsonify(errors='missing candidature'), 400))
    candidature.id_etudiant = id_etudiant
    candidature.voeux = nbVoeux
    candidature.date_candidature = date_candidature
    candidature.deadline_dossier = deadline_dossier
    candidature.validationPE = validationPE
    candidature.id_formation = id_formation

    db.session.commit()
    return jsonify(candidature.serialize())


# ----------------------------FORMATION
@app.route('/api/formation/registration', methods=['POST'])
@auth.login_required
def formation_registration():
    specialite = request.json.get('specialite')
    description = request.json.get('description')
    site_web_url = request.json.get('site_web_url')
    brochure_url = request.json.get('brochure_url')
    alternance = request.json.get('alternance')
    type_formation = request.json.get('type_formation')
    id_responsable = request.json.get('id_responsable')
    id_ecole = request.json.get('id_ecole')
    niveau = request.json.get('niveau')

    if specialite is None or description is None:
        abort(400)
    ecole = Ecole.query.filter_by(id_ecole=id_ecole).first()
    if ecole is None:
        abort(400)

    formation = Formation.query.filter_by(specialite=specialite, id_ecole=id_ecole).first()
    if formation is not None:
        abort(400)
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    form = Formation(id_ecole=id_ecole)
    form.specialite = specialite
    form.description = description
    form.site_web_url = site_web_url
    form.brochure_url = brochure_url
    form.alternance = bool(int(alternance))
    form.niveau = int(niveau)
    form.type_formation = bool(0)
    form.id_responsable = id_responsable
    form.id_ecole = ecole.id_ecole

    db.session.add(form)
    db.session.commit()
    return jsonify(form.serialize())


@app.route('/api/formations/', methods=['GET'])
@auth.login_required
def get_formations():
    info = Formation.query.order_by(Formation.id_ecole).all()
    data = []
    for u in info:

        us = u.serialize()

        if u.id_responsable is None:
            print("pas de id resp")
        else:

            r = ResponsableFormation.query.filter_by(id_responsable=u.id_responsable).first()
            if r is None:
                print("pas de resp")
            else:
                us["responsable"] = r.serialize()
        if u.id_ecole is None:
            print("pas d'ecole")
        else:
            e = Ecole.query.filter_by(id_ecole=u.id_ecole).first()
            us["nom_ecole"] = e.nom_ecole
            fs = Formation.query.filter_by(id_ecole=u.id_ecole).all()
            if fs is not None:
                fdata = []
                for f in fs:
                    if u.id_formation != f.id_formation:
                        fdata.append({"id_formation": f.id_formation, "specialite": f.specialite})

                us['formations'] = fdata
        infoforum = db.session.query(ForumInfo, ParticipationForum).filter(
            ForumInfo.id_forum_info == ParticipationForum.id_forum_info).add_columns()

        infoforum = ForumInfo.query.join(ParticipationForum).filter(
            ParticipationForum.id_formation == u.id_formation).first()

        if infoforum is not None:
            us['ForumInfo'] = infoforum.serialize()
        print(us)
        data.append(us)
    if not info:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/formation/<int:id>', methods=['GET'])
@auth.login_required
def get_formation(id):
    formation = Formation.query.filter_by(id_formation=id).first()

    if formation is None:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify(formation.serialize())


@app.route('/api/formation/<int:id>', methods=['POST'])
@auth.login_required
def update_formation(id):
    specialite = request.json.get('specialite')
    description = request.json.get('description')
    site_web_url = request.json.get('site_web_url')
    brochure_url = request.json.get('brochure_url')
    alternance = request.json.get('alternance')
    type_formation = request.json.get('type_formation')
    id_responsable = request.json.get('id_responsable')
    id_ecole = request.json.get('id_ecole')

    if specialite is None or description is None:
        abort(400)
    ecole = Ecole.query.filter_by(id_ecole=id_ecole).first()
    if ecole is None:
        abort(400)

    formation = Formation.query.filter_by(id_formation=id).first()
    if formation is None:
        abort(400)
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    formation.id_ecole = id_ecole
    formation.specialite = specialite
    formation.description = description
    formation.site_web_url = site_web_url
    formation.brochure_url = brochure_url
    formation.alternance = alternance
    formation.type_formation = type_formation
    formation.id_responsable = id_responsable
    formation.id_ecole = ecole.id_ecole

    db.commit()
    return jsonify(formation.serialize())

@app.route("/api/formation/all", methods=["DELETE"])
@auth.login_required
def formation_delete():
    print("del formation")
    if g.user.rank != Rank.ADMIN.value :
        abort(403)
    formations = Formation.query.order_by(Formation.id_ecole).all()
    for f in formations:
        db.session.delete(f)
    db.session.commit()
    return jsonify({'message':'done'})

# ----------------------------PROFILRECRUTE
@app.route('/api/profilerecrute/registratoin', methods=['POST'])
@auth.login_required
def profilerecrute_registration():
    id_formation = request.json.get('id_formation')
    id_profil = request.json.get('id_profil')

    if id_formation is None or id_profil is None:
        abort(400)

    pr = ProfilRecruter.query.filter_by(id_profil=id_profil, id_formation=id_formation).first()
    if pr is not None:
        abort(400)

    p = Profil.query.filter_by(id_profil=id_profil).first()
    f = Profil.query.filter_by(id_formation=id_formation).first()

    if p is None or f is None:
        abort(400)

    pr = ProfilRecruter()
    pr.id_profil = id_profil
    pr.id_formation = id_formation
    db.session.add(pr)
    db.commit()
    return jsonify(pr.serialize())


@app.route('/api/profilrecrute/', methods=['GET'])
@auth.login_required
def get_profilrecrutes():
    info = ProfilRecruter.query.order_by(ProfilRecruter.id_profil).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/profilrecrute/<int:id>', methods=['GET'])
@auth.login_required
def get_profilrecrute(id):
    pr = ProfilRecruter.query.filter_by(id_profil_recruter=id).first()

    if pr is None:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify(pr.serialize())


@app.route('/api/profilrecrute/<int:id>', methods=['POST'])
@auth.login_required
def update_profilrecrute(id):
    id_formation = request.json.get('id_formation')
    id_profil = request.json.get('id_profil')

    if id_formation is None or id_profil is None:
        abort(400)

    pr = ProfilRecruter.query.filter_by(id_profil_recruter=id).first()
    if pr is None:
        abort(400)

    p = Profil.query.filter_by(id_profil=id_profil).first()
    f = Profil.query.filter_by(id_formation=id_formation).first()

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    if p is None or f is None:
        abort(400)

    pr.id_profil = id_profil
    pr.id_formation = id_formation
    db.commit()
    return jsonify(pr.serialize())


# ----------------------------PROFIL
@app.route('/api/profil/registratoin', methods=['POST'])
@auth.login_required
def profil_registration():
    nom_profil = request.json.get('nom_profil')
    pr = Profil.query.filter_by(nom_profil=nom_profil).first()
    if pr is not None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    pr = Profil(nom_profil=nom_profil)
    db.session.add(pr)
    db.commit()
    return jsonify(pr.serialize())


@app.route('/api/profils/', methods=['GET'])
@auth.login_required
def get_profils():
    info = Profil.query.order_by(Profil.id_profil).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/profil/<int:id>', methods=['GET'])
@auth.login_required
def get_profil(id):
    pr = Profil.query.filter_by(id_profil=id).first()

    if pr is None:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify(pr.serialize())


@app.route('/api/profil/<int:id>', methods=['POST'])
@auth.login_required
def update_profil(id):
    nom_profil = request.json.get('nom_profil')
    id_profil = request.json.get('id_profil')

    if nom_profil is None or id_profil is None:
        abort(400)

    pr = Profil.query.filter_by(id_profil=id).first()
    if pr is None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    pr.id_profil = id_profil
    pr.nom_profil = nom_profil
    db.commit()
    return jsonify(pr.serialize())


# ----------------------------ACTIONPE
@app.route('/api/actionpe/registration', methods=['POST'])
@auth.login_required
def actionpe_registration():
    action = request.json.get('action')
    id_etudiant = request.json.get('id_etudiant')
    id_candidature = request.json.get('id_candidature')

    if action is None or id_etudiant is None or id_candidature is None:
        abort(make_response(jsonify(errors='missing parameters'), 400))

    etu = User.query.filter_by(id=id_etudiant).first()
    can = Candidature.query.filter_by(id_candidature=id_candidature).first()

    if etu is None or can is None:
        abort(make_response(jsonify(errors='Error parameters'), 400))

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(make_response(jsonify(errors='Forbiden'), 403))

    ap = actionPE()
    ap.action = action
    ap.id_etudiant = id_etudiant
    ap.id_candidature = id_candidature
    db.session.add(ap)
    db.session.commit()
    return jsonify(ap.serialize())


@app.route('/api/actionpes/', methods=['GET'])
@auth.login_required
def get_actionpes():
    info = actionPE.query.order_by(actionPE.id_etudiant).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/actionpe/count_user/<int:id>', methods=['GET'])
@auth.login_required
def get_count_user_actionpe(id):
    ap = actionPE.query.filter_by(id_etudiant=id,lu=0).count()

    print(ap)
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify({'nb':ap})

@app.route('/api/actionpe/count/<int:id>', methods=['GET'])
@auth.login_required
def get_count_actionpe(id):
    ap = actionPE.query.filter_by(id_candidature=id,lu=0).count()

    print(ap)
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify({'nb':ap})

@app.route('/api/actionpe/<int:id>', methods=['GET'])
@auth.login_required
def get_actionpe(id):
    ap = actionPE.query.filter_by(id_candidature=id).all()

    data= []
    for u in ap:
        u.lu = 1
        db.session.commit()
        data.append(u.serialize())
    print(data)
    if ap is None:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify(data)


@app.route('/api/actionpe/<int:id>', methods=['POST'])
@auth.login_required
def update_actionpe(id):
    action = request.json.get('action')
    id_etudiant = request.json.get('id_etudiant')
    id_candidature = request.json.get('id_candidature')

    if action is None or id_etudiant is None or id_candidature is None:
        abort(400)

    etu = User.query.filter_by(id_user=id_etudiant).first()
    can = Candidature.query.filter_by(id_candidature=id_candidature).first()
    ap = actionPE.query.filter_by(id_action=id).first()
    if etu is None or can is None or ap is None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    ap.action = action
    ap.id_etudiant = id_etudiant
    ap.id_candidature = id_candidature

    db.commit()
    return jsonify(ap.serialize())


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
        u = User(mail="admin@admin.fr")
        u.hash_password("azerty")
        u.rank=0
        db.session.add(u)
        db.session.commit()

        u = User(mail='martin.rousselle@pe-gmp.fr')
        u.hash_password('azerty')
        u.rank=2
        db.session.add(u)
        db.session.commit()
        
        u = User(mail="oriane@pe-gmp.fr")
        u.hash_password("azerty")
        u.rank=0
        db.session.add(u)
        db.session.commit()
        
        u = User(mail="sonia@admin.fr")
        u.hash_password("azerty")
        u.rank=0
        db.session.add(u)
        db.session.commit()

        type = TypeEcole(nom_type='Publique')
        db.session.add(type)
        db.session.commit()

        type = TypeEcole(nom_type='Privée')
        db.session.add(type)
        db.session.commit()

        ecole = Ecole(nom_ecole='ITII')
        ecole.id_type_ecole = 1
        ecole.id_adresse_ecole = 1
        ecole.description='bla'
        ecole.complement_ecole='site'
        db.session.add(ecole)
        db.session.commit()
    app.run(debug=True,host='0.0.0.0',port=8500)

