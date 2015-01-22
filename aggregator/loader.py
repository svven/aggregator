"""
Aggregator loader from database.
"""
from . import config, db
from itertools import chain

from models import \
    Link as AggregatorLink, Reader as AggregatorReader
from database.news.models import \
    Link as DatabaseLink, Reader as DatabaseReader, Mark as DatabaseMark


class MixedLink(DatabaseLink, AggregatorLink):
  pass
class MixedReader(DatabaseReader, AggregatorReader):
    pass

def load():
    "Load all marks of all readers."
    session = db.Session()
    for reader in session.query(MixedReader).yield_per(100):
        marks = list(chain(*[
            (m.link_id, m.moment) for m in reader.marks.\
            order_by(DatabaseMark.moment).limit(config.MARKS_COUNT)
        ]))
        reader.mark(*marks)
    session.close()
