import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Hardcode values
    TEMPLATES_AUTO_RELOAD = True

    # DB config
    SQLALCHEMY_DATABASE_URI = os.environ.get('MySQL_DB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
