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
    mail = db.Column(db.String(128))
    genre = db.Column(db.Integer)

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
            'username': self.username,
            'mail': self.mail,
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
    id_adresse= db.Column(db.Integer, primary_key=True)
    num_rue = db.Column(db.String(128))
    nom_rue = db.Column(db.String(128))
    ville = db.Column(db.String(128))
    cp = db.Column(db.String(128))
    pays = db.Column(db.String(128))

class ResponsableFormation(db.Model):
    __tablename__ = 'ResponsableFormation'
    id_responsable = db.Column(db.Integer, primary_key=True)
    nom_responsable = db.Column(db.String(128))
    mail_responsable =  db.Column(db.String(128))
    telephone_responsable =  db.Column(db.String(128))



class Candidature(db.Model):
    __tablename__ = 'Candidature'
    id_candidature = db.Column(db.Integer, primary_key=True)
    id_etudiant = db.Column(db.Integer, db.ForeignKey('User.id'))
    id_voeux = db.Column(db.Integer, db.ForeignKey('Voeux.id_voeux'))
    date_candidature = db.Column(db.Integer)

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

class ProfilRecruter(db.Model):
    __tablename__ = 'ProfilRecruter'
    id_profil_recruter = db.Column(db.Integer, primary_key=True)
    id_formation = db.Column(db.Integer, db.ForeignKey('Formation.id_formation'))
    id_profil = db.Column(db.Integer, db.ForeignKey('Profil.id_profil'))

class Profil(db.Model):
    __tablename__ = 'Profil'
    id_profil =  db.Column(db.Integer, primary_key=True)
    nom_profil = db.Column(db.String(128))

class Voeux(db.Model):
    __tablename__ = 'Voeux'
    id_voeux = db.Column(db.Integer, primary_key=True)
    ordre = db.Column(db.Integer)
    deadline_dossier = db.Column(db.Integer)
    validationPE = db.Column(db.Boolean)

class actionPE(db.Model):
    __tablename__ = 'actionPE'
    id_action = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    etudiant = db.Column(db.Integer, db.ForeignKey('User.id'))
    voeux = db.Column(db.Integer, db.ForeignKey('Voeux.id_voeux'))


@app.route('/')
def get_api_endpoint():
    return jsonify(api_endpoint())


@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()

    app.run(debug=True)
