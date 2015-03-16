"""
Aggregator models: Reader, Link

Note: Moment may refer to:
<https://www.google.com/search?q=define+moment>
  1. a very brief period of time.
  synonyms: bit, minute, instant, second, split second;
  2. importance.
  synonyms: importance, significance, weight;
"""
from __future__ import division

import config, keys, scripts
from . import r

from config import BASE_UXTIME, \
	FELLOWS_COUNT, NEWS_COUNT, MARKS_COUNT, MARKS_LIMIT
from keys import \
	LINK_MARKERS, READER_MARKS, READER_FELLOWS, READER_EDITION

AD = lambda m: m is not None and m/BASE_UXTIME or None # anno Domini


class Link(object):
	"""
	Link class to cache link data.
	"""
	def __init__(self, id=None):
		"Simple init."
		self.id = id

	# Getter methods
	def get_markers(self, withscores=False):
		"Return all readers that marked the link."
		return r.zrange(keys.get(LINK_MARKERS, self.id),
			0, -1, desc=True, withscores=withscores)


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
		scripts.mark(keys=[self.id], args=[AD(moment), link_id])

	def mark(self, *marks):
		"""
		Bulk record the marks specified as [link_id, moment, ..]
		"""
		args = []
		for i in xrange(0, len(marks), 2):
			link_id, moment = (marks[i], marks[i+1])
			args.extend([AD(moment), link_id])
		scripts.mark(keys=[self.id], args=args)

	def unmark(self, link_id):
		"Remove link_id from reader_id marks."
		scripts.unmark(keys=[self.id], args=[link_id])

	# Getter methods. Pass count 0 to return all
	def get_marks(self, count=MARKS_COUNT, withscores=False):
		"Return latest reader marks as links."
		return r.zrange(keys.get(READER_MARKS, self.id),
			0, count-1, desc=True, withscores=withscores)

	def get_fellows(self, count=FELLOWS_COUNT, withscores=False):
		"Return fellows as readers based on recorded marks."
		# self.set_fellows() # real time
		return r.zrange(keys.get(READER_FELLOWS, self.id), 
			0, count-1, desc=True, withscores=withscores)

	def get_edition(self, count=NEWS_COUNT, withscores=False):
		"Return news edition as links based on fellows."
		# self.set_edition() # real time
		return r.zrange(keys.get(READER_EDITION, self.id), 
			0, count-1, desc=True, withscores=withscores)

	# Setter methods or aggregations
	def aggregate(self,
		moment_min=None, moment_max=None):
		"Refresh fellows and edition aggregations."
		self.set_fellows(moment_min=moment_min, moment_max=moment_max)
		self.set_edition(moment_min=moment_min, moment_max=moment_max)

	def set_fellows(self, 
		moment_min=None, moment_max=None, marks_count=MARKS_COUNT):
		"Aggregate fellows based on marks inside moments interval."
		scripts.set_fellows(keys=[self.id], 
			args=[AD(moment_min), AD(moment_max), marks_count])

	def set_edition(self,
		moment_min=None, moment_max=None, fellows_count=FELLOWS_COUNT):
		"Aggregate edition from moments interval based on fellows."
		scripts.set_edition(keys=[self.id],
			args=[AD(moment_min), AD(moment_max), fellows_count])

	# Maintenance methods
	def rem_marks(self, keep=MARKS_LIMIT):
		"Remove old marks, keep as many as specified."
		scripts.rem_marks(keys=[self.id], args=[keep])
