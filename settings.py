import os



class Config(object):
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5001

    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = '$%UHGD#O%$^htrfgolk546-fd[ssk;435gf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(ROOT_PATH, 'database.db')
    # postgresql://scott:tiger@localhost/mydatabase

    
    TEMPLATES_FOLDER = os.path.join(ROOT_PATH, 'templates')
    STATIC_FOLDER = os.path.join(ROOT_PATH, 'static')
    FOLDER_MEDIA = 'media'

    FOLDER_USER = os.path.join(FOLDER_MEDIA, 'user')
    FOLDER_MOVIE = os.path.join(FOLDER_MEDIA, 'movie')
    FOLDER_PRODUCER = os.path.join(FOLDER_MEDIA, 'producer')


    ALLOWED_EXTENSIONS = ["jpg", "png", "jpeg"]
    MAX_CONTENT_LENGTH = 3000 * 1024  # 3 mb


    # number_items_page = 3
    # NUMBER_ITEMS_PAGE = 3

    # SECURITY_PASSWORD_SALT = 'flask-solt-security'
    # SECURITY_PASSWORD_HASH = 'bcrypt'
