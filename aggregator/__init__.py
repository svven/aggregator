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

def load(count=config.PICKS_LIMIT):
    "Load latest reader picks from database."
    from mixes import MixedReader
    from database.models import Pick, Link
    from itertools import chain

    for reader in MixedReader.query.yield_per(100):
        if reader.ignored:
            continue
        picks = list(chain(*[
            (m.link_id, m.moment) for m in Pick.query.join(Link).\
            filter(Pick.reader_id == reader.id, 
                (Link.ignored == None) | (Link.ignored == False)).\
            order_by(Pick.moment.desc()).limit(count)
        ]))
        if picks:
            reader.pick(*picks)

def aggregate():
    "Aggregate all loaded reader picks."
    from mixes import MixedReader

    for reader in MixedReader.query.yield_per(100):
        if reader.ignored:
            continue
        reader.aggregate()

def clean(keep=config.PICKS_LIMIT):
    "Remove old picks."
    from mixes import MixedReader

    for reader in MixedReader.query.yield_per(100):
        if reader.ignored:
            continue
        reader.rem_picks(keep)
