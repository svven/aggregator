"""
Aggregator intitialization.
"""
import config

import database, redis

def load_config(updates=None):
	"""
	Delayed init to allow config updates.
	Updates can be passed as param here or set onto `config` upfront.
	i.e. `config.SETTING = updates.PREFIX_SETTING or updates.SETTING`
	"""
	def update_config():
		"Update same name (or prefixed) settings in config."
		prefix = config.__name__.split('.')[0].upper()
		keys = [k for k in config.__dict__ if not k.startswith('_')]
		get_value = lambda c, k: hasattr(c, k) and getattr(c, k) or None
		for key in keys:
			prefix_key = '%s_%s' % (prefix, key)
			value = get_value(updates, prefix_key) or get_value(updates, key)
			if value: setattr(config, key, value)
	if updates:
		update_config()

	global db, r

	## Database
	database.config.sqlalchemy_url = config.sqlalchemy_url
	database.config.SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI
	db = database.db

	## Redis
	r = redis.StrictRedis(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)

	## Models
	from models import Link, Reader # delayed
