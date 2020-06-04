import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
path_to_env = os.path.join(basedir, '.env')
load_dotenv(path_to_env)


class Config(object):
    # database URL's, config, etc.
    DATABASE_URL = os.getenv("DATABASE_URL")
    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    SECRET_KEY     = os.getenv("SECRET_KEY")

    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
