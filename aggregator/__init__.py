"""
Aggregator intitialization.
"""
import config

# TODO: Make this generic
database.config.sqlalchemy_url = config.sqlalchemy_url
database.config.SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI

import database
db = database.db


import redis
r = redis.StrictRedis(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)

from models import *
