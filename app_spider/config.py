import os
import configparser
from hashlib import md5

current_file_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(os.path.split(current_file_path)[0],"config.ini")
cf = configparser.ConfigParser()
cf.read(config_path)

db_host = cf.get("DEFAULT", "db_host")
db_port = cf.get("DEFAULT", "db_port")
db_user = cf.get("DEFAULT", "db_user")
db_password = cf.get("DEFAULT", "db_password")
db_username = cf.get("DEFAULT", "db_username")
db_name = cf.get("DEFAULT", "db_name")
log_file = cf.get("DEFAULT", "log_file")
error_log_file = cf.get("DEFAULT", "error_log")

LOGIN_EXPIRE_TIME_SECONDS = 3600 * 2

class ConfigObject():
    SECRET_KEY = md5("spider_api".encode("utf-8")).hexdigest()
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    CSRF_ENABLED = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (db_username, db_password, db_host, db_port, db_name)
    # MAX_CONTENT_LENGTH = 10 * 1024 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_MAX_OVERFLOW = 1000
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 30
