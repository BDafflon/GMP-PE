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
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id_forum_info': self.id_forum_info,
            'lien_visio': self.lien_visio,
            'lien_video': self.lien_video

        }


class ParticipationForum(db.Model):
    __tablename__='ParticiationForum'
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
            'anne':self.annee
        }

class TypeEcole(db.Model):
    __tablename__ = 'TypeEcole'
    id_type_ecole = db.Column(db.Integer, primary_key=True)
    nom_type = db.Column(db.String(128))
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id_type_ecole': self.id_type_ecole,
            'nom_type': self.nom_type
        }


class Ecole(db.Model):
    __tablename__ = 'Ecole'
    id_ecole = db.Column(db.Integer, primary_key=True)
    nom_ecole = db.Column(db.String(128))
    id_type_ecole = db.Column(db.Integer, db.ForeignKey('TypeEcole.id_type_ecole'))
    id_adresse_ecole = db.Column(db.Integer, db.ForeignKey('Adresse.id_adresse'))

    def serialize(self):
        return {
            'id_ecole': self.id_ecole,
            'nom_ecole': self.nom_ecole,
            'id_type_ecole':self.id_type_ecole,
            'id_adresse_ecole':self.id_adresse_ecole
        }


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
            'nom_rue':self.nom_rue,
            'ville':self.ville,
            'cp':self.cp,
            'pays':self.pays
        }

class ResponsableFormation(db.Model):
    __tablename__ = 'ResponsableFormation'
    id_responsable = db.Column(db.Integer, primary_key=True)
    nom_responsable = db.Column(db.String(128))
    mail_responsable = db.Column(db.String(128))
    telephone_responsable = db.Column(db.String(128))
    def serialize(self):
        return {
            'id_responsable': self.id_responsable,
            'nom_responsable': self.nom_responsable,
            'mail_responsable':self.mail_responsable,
            'telephone_responsable':self.telephone_responsable
        }


class Candidature(db.Model):
    __tablename__ = 'Candidature'
    id_candidature = db.Column(db.Integer, primary_key=True)
    id_etudiant = db.Column(db.Integer, db.ForeignKey('User.id'))
    id_voeux = db.Column(db.Integer, db.ForeignKey('Voeux.id_voeux'))
    date_candidature = db.Column(db.Integer)
    deadline_dossier = db.Column(db.Integer)
    validationPE = db.Column(db.Boolean)
    voeux = db.Column(db.Integer)
    id_formation = db.Column(db.Integer, db.ForeignKey('Formation.id_formation'))
    def serialize(self):
        return {
            'id_candidature': self.id_candidature,
            'id_etudiant': self.id_etudiant,
            'id_voeux':self.id_voeux,
            'date_candidature':self.date_candidature,
            'deadline_dossier':self.deadline_dossier,
            'validationPE':self.validationPE,
            'id_formation':self.id_formation
        }

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
    return jsonify(user.serialize())


# ----------------------------ForumInfo
@app.route('/api/foruminfo/registratoin', methods=['POST'])
@auth.login_required
def foruminfo_registration():
    lien_visio = request.json.get('lien_visio')
    lien_video = request.json.get('lien_video')

    if lien_visio is None or lien_video is None :
        abort(400)

    if g.user.rank != Rank.ADMIN.value :
        abort(403)

    info = ForumInfo(lien_visio=lien_visio)
    info.lien_video = lien_video
    db.session.add(info)
    db.session.commit()
    return jsonify(info.serialize())



@app.route('/api/foruminfo/', methods=['GET'])
@auth.login_required
def get_foruminfos():
    info = ForumInfo.query.order_by(ForumInfo.id_forum_info).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        return jsonify({})
    print(g.user.serialize())

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    return jsonify(data)


@app.route('/api/foruminfo/<int:id>', methods=['GET'])
@auth.login_required
def get_foruminfo(id):
    info = ForumInfo.query.filter_by(id_forum_info=id).first()

    if not info:
        return jsonify({})
    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    return jsonify(info.serialize())


@app.route('/api/foruminfo/<int:id>', methods=['POST'])
@auth.login_required
def update_forum(id):
    lien_visio = request.json.get('lien_visio')
    lien_video = request.json.get('lien_video')

    if lien_visio is None or lien_video is None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    info = ForumInfo.query.filter_by(id_forum_info=id).first()
    if not info:
        abort(400)
    info.lien_visio = lien_visio
    info.lien_video = lien_video
    db.session.commit()
    return jsonify(info.serialize())


#-----------------------------ParticipationForum
@app.route('/api/participationforum/registratoin', methods=['POST'])
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
    info.annee= int(annee)
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
@app.route('/api/typeecole/registratoin', methods=['POST'])
@auth.login_required
def typeecole_registration():
    nom_type = request.json.get('nom_type')

    if nom_type is None :
        abort(400)

    if g.user.rank != Rank.ADMIN.value:
        abort(403)

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
        return jsonify({})
    print(g.user.serialize())

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

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
@app.route('/api/typeecole/registratoin', methods=['POST'])
@auth.login_required
def ecole_registration():
    nom_ecole = request.json.get('nom_ecole')
    id_type_ecole = request.json.get('id_type_ecole')
    id_adresse_ecole = request.json.get('id_adresse_ecole')


    if nom_ecole is None or id_type_ecole is None or id_adresse_ecole is None  :
        abort(400)
    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    ecole = Ecole.query.filter_by(nom_ecole=nom_ecole).first()
    adresse = Adresse.query.filter_by(id_adresse=id_adresse_ecole).first()
    type = TypeEcole.query.filter_by(id_type=id_type_ecole).first()
    if ecole is not None:
        abort(400)
    if type is None or adresse is None:
        abort(400)

    ecole = Ecole(nom_ecole=nom_ecole)
    ecole.id_type_ecole = int(id_type_ecole)
    ecole.id_adresse_ecole = int(id_adresse_ecole)
    db.session.add(ecole)
    db.session.commit()
    return jsonify(ecole.serialize())

@app.route('/api/ecoles/', methods=['GET'])
@auth.login_required
def get_ecoles():
    info = Ecole.query.order_by(Ecole.nom_ecole).all()
    data = []
    for u in info:
        data.append(u.serialize())
    if not info:
        return jsonify({})
    print(g.user.serialize())

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
    type = TypeEcole.query.filter_by(id_type=id_type_ecole).first()
    if ecole is None:
        abort(400)
    if type is None or adresse is None:
        abort(400)


    ecole.id_type_ecole = int(id_type_ecole)
    ecole.id_adresse_ecole = int(id_adresse_ecole)
    ecole.nom_ecole=nom_ecole
    db.session.commit()
    return jsonify(ecole.serialize())


# ----------------------------ADRESSE
@app.route('/api/adresse/registratoin', methods=['POST'])
@auth.login_required
def adresse_registration():
    num_rue = request.json.get('num_rue')
    nom_rue = request.json.get('nom_rue')
    ville = request.json.get('ville')
    cp = request.json.get('cp')
    pays = request.json.get('pays')

    if num_rue is None or nom_rue is None or ville is None or cp is None or pays is None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    adresse = Adresse.query.filter_by(num_rue=num_rue,nom_rue=nom_rue,ville=ville,cp=cp,pays=pays).first()
    if adresse is not None:
        abort(400)

    adr = Adresse(num_rue=num_rue)
    adr.nom_rue=nom_rue
    adr.ville=ville
    adr.cp=cp
    adr.pays=pays
    db.session.add(adr)
    db.commit()
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

    return jsonify(data)


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
@app.route('/api/responsable/registratoin', methods=['POST'])
@auth.login_required
def responsable_registration():
    nom_responsable = request.json.get('nom_responsable')
    mail_responsable = request.json.get('mail_responsable')
    telephone_responsable = request.json.get('telephone_responsable')

    if nom_responsable is None or mail_responsable is None or telephone_responsable is None:
        abort(400)
    if g.user.rank != Rank.ADMIN.value:
        abort(403)

    res = ResponsableFormation.query.filter_by(nom_responsable=nom_responsable,mail_responsable=mail_responsable).first()
    if res is not None :
        abort(400)

    resp = ResponsableFormation(nom_responsable=nom_responsable)
    resp.mail_responsable = mail_responsable
    resp.telephone_responsable = telephone_responsable
    db.session.add(resp)
    db.commit()
    return jsonify(resp.serialize())

@app.route('/api/responsable/', methods=['GET'])
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

    resp.nom_responsable=nom_responsable
    resp.mail_responsable = mail_responsable
    resp.telephone_responsable = telephone_responsable
    db.commit()
    return jsonify(resp.serialize())


# ----------------------------CANDIDATURE
@app.route('/api/candidature/registratoin', methods=['POST'])
@auth.login_required
def candidature_registration():
    id_etudiant = request.json.get('id_etudiant')
    date_candidature = request.json.get('date_candidature')
    deadline_dossier = request.json.get('deadline_dossier')
    validationPE = request.json.get('validationPE')
    id_formation = request.json.get('id_formation')

    if id_etudiant is None is None or date_candidature is None or deadline_dossier is None or validationPE is None or id_formation is None :
        abort(400)
    etu = User.query.filter_by(id_etudiant=id_etudiant).first()
    formation = Formation.query.filter_by(id_formation=id_formation).first()
    if etu is None or formation is None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)
    nbVoeux = len(Candidature.query.filter_by(id_user=id_etudiant))



    candidature = Candidature(id_etudiant=id_etudiant)
    candidature.id_voeux = nbVoeux+1
    candidature.date_candidature=date_candidature
    candidature.deadline_dossier=deadline_dossier
    candidature.validationPE=validationPE
    candidature.id_formation = id_formation

    db.commit()
    return jsonify(candidature.serialize())

@app.route('/api/candidature/', methods=['GET'])
@auth.login_required
def get_candidatures():
    info = Candidature.query.order_by(Candidature.id_etudiant).all()
    data = []
    for u in info:
        data.append(u.serialize())
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
    if id_etudiant is None is None or date_candidature is None or deadline_dossier is None or validationPE is None or id_formation is None:
        abort(400)
    etu = User.query.filter_by(id_etudiant=id_etudiant).first()
    formation = Formation.query.filter_by(id_formation=id_formation).first()
    if etu is None or formation is None:
        abort(400)

    if g.user.rank != Rank.ADMIN.value and g.user.rank != Rank.USER.value:
        abort(403)

    candidature = Candidature.query.filter_by(id_candidature=id).first()
    if candidature is None:
        abort(400)
    candidature.id_etudiant=id_etudiant
    candidature.id_voeux = nbVoeux
    candidature.date_candidature = date_candidature
    candidature.deadline_dossier = deadline_dossier
    candidature.validationPE = validationPE
    candidature.id_formation = id_formation

    db.commit()
    return jsonify(candidature.serialize())


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
