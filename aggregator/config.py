"""
Config settings for aggregator.
"""

## SQLAlchemy
## http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
# SQLALCHEMY_ECHO = sqlalchemy_echo = True
SQLALCHEMY_DATABASE_URI = sqlalchemy_url = 'postgresql://svven@localhost/svven'

## Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PREFIX = 'aggregator'

## Aggregator
FELLOWS_COUNT = 30
NEWS_COUNT = 30
MARKS_COUNT = 30

BASE_UXTIME = 0 # 1388534400 # datetime(2014, 1, 1, 0, 0)
