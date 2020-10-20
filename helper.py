from enum import Enum


import random
import string


UPLOAD_FOLDER = 'file/upload/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str



class Rank(Enum):
    ADMIN=0
    APP=1
    USER=2

def api_endpoint():
    return {}