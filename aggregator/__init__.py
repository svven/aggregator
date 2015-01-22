"""
Aggregator intitialization.
"""
import config

import database, redis

def load_config():
	"Delayed init to allow config updates."
	global db, r

	## Database
	database.config.sqlalchemy_url = config.sqlalchemy_url
	database.config.SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI
	db = database.db

	## Redis
	r = redis.StrictRedis(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)

	## Models
	from models import * # delayed
