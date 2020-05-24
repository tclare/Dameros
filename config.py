import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
path_to_env = os.path.join(basedir, '.env')
load_dotenv(path_to_env)


class Config(object):
    # database URL's, config, etc.
    DATABASE_URL = os.getenv("DATABASE_URL")
