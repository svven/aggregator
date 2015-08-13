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

from keys import \
    LINK_PICKERS, READER_PICKS, READER_FELLOWS, READER_EDITION, EDITION_FELLOWS

AD = lambda m: m is not None and m/config.BASE_UXTIME or None # anno Domini


class Link(object):
    """
    Link class to cache link data.
    """
    def __init__(self, id=None):
        "Simple init."
        self.id = id

    # Getter methods
    def get_pickers(self, withscores=False):
        "Return all readers that picked the link."
        return r.zrange(keys.get(LINK_PICKERS, self.id),
            0, -1, desc=True, withscores=withscores)

    # Maintenance methods
    def rem_picks(self):
        "Remove all link picks."
        scripts.rem_link_picks(keys=[self.id])


class Reader(object):
    """
    Reader class performs the aggregations on demand 
    and provides the picks, fellows and news edition for the reader.
    """
    def __init__(self, id):
        "Simple init."
        self.id = id

    # Special methods
    def pick(self, link_id, moment):
        "Record link_id as pick at specified uxtime moment."
        scripts.pick(keys=[self.id], args=[AD(moment), link_id])

    def pick(self, *picks):
        """
        Bulk record the picks specified as [link_id, moment, ..]
        """
        args = []
        for i in xrange(0, len(picks), 2):
            link_id, moment = (picks[i], picks[i+1])
            args.extend([AD(moment), link_id])
        scripts.pick(keys=[self.id], args=args)

    def unpick(self, link_id):
        "Remove link_id from reader_id picks."
        scripts.unpick(keys=[self.id], args=[link_id])

    # Getter methods. Pass count 0 to return all
    def get_picks(self, count=config.PICKS_COUNT, withscores=False):
        "Return latest reader picks as links."
        return r.zrange(keys.get(READER_PICKS, self.id),
            0, count-1, desc=True, withscores=withscores)

    def get_fellows(self, count=config.FELLOWS_COUNT, withscores=False):
        "Return fellows as readers based on recorded picks."
        # self.set_fellows() # real time
        return r.zrange(keys.get(READER_FELLOWS, self.id), 
            0, count-1, desc=True, withscores=withscores)

    def get_edition(self, count=config.NEWS_COUNT, withscores=False):
        "Return news edition as links based on fellows."
        # self.set_edition() # real time
        return r.zrange(keys.get(READER_EDITION, self.id), 
            0, count-1, desc=True, withscores=withscores)

    def get_edition_fellows(self):
        "Return link fellows from edition."
        return r.hgetall(keys.get(EDITION_FELLOWS, self.id))

    # Setter methods or aggregations
    def aggregate(self,
        moment_min=None, moment_max=None):
        "Refresh fellows and edition aggregations."
        self.set_fellows(moment_min=moment_min, moment_max=moment_max)
        self.set_edition(moment_min=moment_min, moment_max=moment_max)

    def set_fellows(self, 
        moment_min=None, moment_max=None, picks_count=config.PICKS_COUNT):
        "Aggregate fellows based on picks inside moments interval."
        scripts.set_fellows(keys=[self.id], 
            args=[AD(moment_min), AD(moment_max), picks_count])

    def set_edition(self,
        moment_min=None, moment_max=None, fellows_count=config.FELLOWS_COUNT):
        "Aggregate edition from moments interval based on fellows."
        scripts.set_edition(keys=[self.id],
            args=[AD(moment_min), AD(moment_max), fellows_count])

    # Maintenance methods
    def rem_picks(self, keep=config.PICKS_LIMIT):
        "Remove old reader picks, keep as many as specified."
        scripts.rem_reader_picks(keys=[self.id], args=[keep])
