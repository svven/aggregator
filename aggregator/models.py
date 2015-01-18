"""
Aggregator models: Reader, Link

Note: Moment may refer to:
<https://www.google.com/search?q=define+moment>
  1. a very brief period of time.
  synonyms: bit, minute, instant, second, split second;
  2. importance.
  synonyms: importance, significance, weight;
"""
from . import r
import config, keys, scripts, utils

from config import BASE_UXTIME, \
	FELLOWS_COUNT, NEWS_COUNT, MARKS_COUNT
from keys import \
	LINK_MARKERS, READER_MARKS, READER_FELLOWS, READER_EDITION

AD = lambda m: m - BASE_UXTIME # anno Domini


class Link(object):
	"""
	Link class to cache link data.
	"""
	def __init__(self, id=None):
		"Simple init."
		self.id = id

	# Getter methods
	def get_markers(self):
		"Return all readers that marked the link."
		return r.smembers(keys.get(LINK_MARKERS, self.id))


class Reader(object):
	"""
	Reader class performs the aggregations on demand 
	and provides the marks, fellows and news edition for the reader.
	"""
	def __init__(self, id):
		"Simple init."
		self.id = id

	# Special methods
	def mark(self, link_id, moment):
		"Record link_id as mark at specified uxtime moment."
		# r.sadd(keys.get(LINK_MARKERS, link_id), self.id)
		# r.zadd(keys.get(READER_MARKS, self.id), AD(moment), link_id)
		scripts.mark(keys=[self.id], args=[AD(moment), link_id])

	def mark(self, *marks):
		"""
		Bulk record the marks specified as [link_id, moment, ..]
		"""
		link_ids = marks[::2]
		moments = [AD(moment) for moment in marks[1::2]]
		args = utils.unzip(zip(moments, link_ids))
		# # kwargs = dict([(read[0], read[1]) 
		# # 	for read in zip(link_ids, moments)])
		# # r.zadd(keys.get(READER_MARKS, self.id), **kwargs)
		# for link_id in link_ids:
		# 	r.sadd(keys.get(LINK_MARKERS, link_id), self.id)
		# r.zadd(keys.get(READER_MARKS, self.id), *args)
		scripts.mark(keys=[self.id], args=args)

	def unmark(self, link_id):
		"Remove link_id from reader_id marks."
		# r.srem(keys.get(LINK_MARKERS, link_id), self.id)
		# r.zrem(keys.get(READER_MARKS, self.id), link_id)
		scripts.unmark(keys=[self.id], args=[link_id])

	# Getter methods. Pass count 0 to return all
	def get_marks(self, count=MARKS_COUNT):
		"Return latest reader marks as links."
		return r.zrange(keys.get(READER_MARKS, self.id),
			0, count-1, desc=True, withscores=False)

	def get_fellows(self, count=FELLOWS_COUNT):
		"Return fellows as readers based on recorded marks."
		self.set_fellows() # real time
		return r.zrange(keys.get(READER_FELLOWS, self.id), 
			0, count-1, desc=True, withscores=False)

	def get_edition(self, count=NEWS_COUNT):
		"Return news edition as links based on fellows."
		self.set_edition() # real time
		return r.zrange(keys.get(READER_EDITION, self.id), 
			0, count-1, desc=True, withscores=False)

	# Setter methods or aggregations
	def set_fellows(self, marks_count=MARKS_COUNT):
		"Aggregate fellows based on marks."
		# keys = [keys.get(LINK_MARKERS, link_id) for link_id in self.marks[:marks_count]]
		# r.zunionstore(keys.get(READER_FELLOWS, self.id), keys)
		# r.zrem(keys.get(READER_FELLOWS, self.id), self.id)
		scripts.set_fellows(keys=[self.id], args=[marks_count])

	def set_edition(self):
		"Aggregate edition based on fellows."
		# fellows = self.fellows
		# keys = dict([(keys.get(READER_MARKS, fellow[0]), fellow[1]) for fellow in fellows])
		# r.zunionstore(keys.get(READER_EDITION, self.id), keys)
		# r.zrem(keys.get(READER_EDITION, self.id), *self.marks)
		scripts.set_edition(keys=[self.id])
