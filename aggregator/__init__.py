"""
Aggregator intitialization.
"""
import config, database, redis

def init(config_updates=None):
    """
    Delayed init to allow config updates.
    Updates can be passed as param here or set onto `config` upfront.
    i.e. `config.SETTING = updates.PREFIX_SETTING or updates.SETTING`
    """
    if config_updates:
        config.from_object(config_updates)

    global db, r

    ## Database
    database.init(config)
    db = database.db

    ## Redis
    r = redis.StrictRedis(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)

    ## Models
    from models import Link, Reader # delayed because of `r`

def load(count=config.MARKS_LIMIT):
    "Load latest reader marks from database."
    from mixes import MixedReader
    from database.models import Mark
    from itertools import chain

    for reader in MixedReader.query.yield_per(100):
        if reader.ignored:
            continue
        marks = list(chain(*[
            (m.link_id, m.moment) for m in reader.marks.\
            order_by(Mark.moment.desc()).limit(count)
        ]))
        reader.mark(*marks)

def aggregate():
    "Aggregate all loaded reader marks."
    from mixes import MixedReader

    for reader in MixedReader.query.yield_per(100):
        if reader.ignored:
            continue
        reader.aggregate()

def clean(keep=config.MARKS_LIMIT):
    "Remove old marks."
    from mixes import MixedReader

    for reader in MixedReader.query.yield_per(100):
        if reader.ignored:
            continue
        reader.rem_marks(keep)
