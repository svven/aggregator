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
            reader.rem_picks()

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

def ignore(url_or_screen_name):
    """
    Mark as ignored and remove its picks.
    Works for both link by url or reader by screen_name. 
    """
    from mixes import MixedLink, MixedReader
    from database.models import TwitterUser

    from . import db
    session = db.Session()

    if '/' in url_or_screen_name:
        url = url_or_screen_name
        link = session.query(MixedLink).filter_by(url=url).one()
        link.ignored = True
        link.rem_picks()
    else:
        screen_name = url_or_screen_name
        reader = session.query(MixedReader).join(TwitterUser).\
            filter(TwitterUser.screen_name == screen_name).one()
        reader.ignored = True
        reader.rem_picks(0) # keep none

    session.commit()
    session.close()
