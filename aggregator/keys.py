"""
Redis Keys
  * `link_markers:link_id` - set of reader_ids that marked the link_id
  * `reader_marks:reader_id` - zset of (link_id, moment) marked by reader_id
  * `reader_fellows:reader_id` - zset of (fellow_id, moment)
  * `reader_edition:reader_id` - zset of (link_id, moment) aka the 
  relavant news edition
"""
from config import REDIS_PREFIX

KEYS = [
	LINK_MARKERS, READER_MARKS, READER_FELLOWS, READER_EDITION] = [
	'link_markers', 'reader_marks', 'reader_fellows', 'reader_edition'
]

DICT = dict(
	zip(KEYS, [':'.join((REDIS_PREFIX, k, '')) for k in KEYS])
)

def get(key, id=''):
	"Param `key` should be one of the `KEYS`."
	assert key in KEYS, \
		'Missing redis key: %s' % key
	return DICT[key] + str(id)
