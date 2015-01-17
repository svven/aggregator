"""
Aggregator loader from database.
"""
from . import config, db
from itertools import chain

from aggregator import \
    Link as AggregatorLink, Reader as AggregatorReader
from database import \
    Link as DatabaseLink, Reader as DatabaseReader, Mark as DatabaseMark


class ExtendedLink(DatabaseLink, AggregatorLink):
  pass
class ExtendedReader(DatabaseReader, AggregatorReader):
    pass

def load():
    "Load all marks of all readers."
    session = db.Session()
    for reader in session.query(ExtendedReader).yield_per(100):
        reader.reader_id = reader.id
        marks = list(chain(*[
            (m.link_id, m.moment) for m in reader.marks.\
            order_by(DatabaseMark.moment).limit(config.MARKS_COUNT)
        ]))
        reader.mark(*marks)
    session.close()
