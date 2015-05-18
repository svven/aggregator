"""
Redis Keys
  * `link_pickers:link_id` - zset of (reader_id, moment) that picked link_id
  * `reader_picks:reader_id` - zset of (link_id, moment) picked by reader_id
  * `reader_fellows:reader_id` - zset of (fellow_id, moment)
  * `reader_edition:reader_id` - zset of (link_id, moment) aka the 
  relavant news edition
"""
from config import REDIS_PREFIX

KEYS = [
    LINK_PICKERS, READER_PICKS, READER_FELLOWS, READER_EDITION] = [
    'link_pickers', 'reader_picks', 'reader_fellows', 'reader_edition'
]

DICT = dict(
    zip(KEYS, [':'.join((REDIS_PREFIX, k, '')) for k in KEYS])
)

def get(key, id=''):
    "Param `key` should be one of the `KEYS`."
    assert key in KEYS, \
        'Missing redis key: %s' % key
    return DICT[key] + str(id)
