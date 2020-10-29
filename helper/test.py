import random
import string

import requests


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def getUser(id):

    username = "admin"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/user/'+str(id)

    x = requests.get(url, auth=(username, password))

    print(x.json())



def getUsers():

    username = "admin"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/users'

    x = requests.get(url, auth=(username, password))

    print(x.json())

def addRandomUser():
    nom = get_random_string(10)
    prenom = get_random_string(10)
    numero = random.randint(1000,10000)
    password = "azerty"
    groupeTD = ""
    mail = get_random_string(10)+"@admin.fr"

    username = "admin"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/user/registration'
    myobj = {'nom': nom,
             'prenom': prenom,
             'numero':numero,
             'password':password,
             'groupeTD':groupeTD,
             'mail':mail
             }
    x = requests.post(url, json=myobj,auth=(username, password))

    print(x.json())


def updateRandomUser(id):
    nom = get_random_string(10)
    prenom = get_random_string(10)
    numero = random.randint(1000,10000)
    password = "azerty"
    groupeTD = ""
    mail = get_random_string(10)+"@admin.fr"

    username = "admin"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/user/'+str(id)
    myobj = {'nom': nom,
             'prenom': prenom,
             'numero':numero,
             'password':password,
             'groupeTD':groupeTD,
             'mail':mail
             }
    x = requests.post(url, json=myobj,auth=(username, password))

    print(x.json())

def addRandomAdress():
    num_rue = 10
    nom_rue = "rue pailleron"
    ville = "Lyon"
    cp = "69003"
    pays = "France"

    username = "admin@admin.fr"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/adresse/registration'
    myobj = {
            'num_rue': num_rue,
             'nom_rue': nom_rue,
             'ville': ville,
             'cp':cp,
             'pays':pays
             }
    x = requests.post(url, json=myobj, auth=(username, password))

    print(x)


def addRandomforuminfo():
    visio = get_random_string(10)
    video = get_random_string(10)

    username = "admin"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/foruminfo/registration'
    myobj = {'lien_visio': visio,
             'lien_video': video
             }
    x = requests.post(url, json=myobj,auth=(username, password))

    print(x.json())


def getforuminfos(id):

    username = "admin"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/foruminfo/'+str(id)

    x = requests.get(url, auth=(username, password))

    print(x.json())

def updateRandomforuminfo(id):
    visio = get_random_string(10)
    video = get_random_string(10)

    username = "admin"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/foruminfo/'+str(id)
    myobj = {'lien_visio': visio,
             'lien_video': video
             }
    x = requests.post(url, json=myobj,auth=(username, password))

    print(x.json())


def addRandomtypeecole():
    type = get_random_string(10)


    username = "admin"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/typeecole/registration'
    myobj = {'nom_type': type
             }
    x = requests.post(url, json=myobj,auth=(username, password))

    print(x.json())

def typeecole(id):

    username = "admin"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/foruminfo/'+str(id)

    x = requests.get(url, auth=(username, password))

    print(x.json())

def getToken():

    username = "admin@admin.fr"
    password = "azerty"

    url = 'http://127.0.0.1:5000/api/token'

    x = requests.post(url, auth=(username, password))

    print(x.text)

#addRandomUser()
#getUsers()
#getUser(4)
#updateRandomUser(2)
#addRandomforuminfo()
addRandomAdress()

#getforuminfos(3)
#updateRandomforuminfo(1)
#addRandomtypeecole()
