"""
Mixed models: Reader, Link
"""
from models import \
    Link as AggregatorLink, Reader as AggregatorReader
from database.models import \
    Link as DatabaseLink, Reader as DatabaseReader


class MixedLink(DatabaseLink, AggregatorLink):
    """
    Link mix from database and aggregator.
    """
    pass


class MixedReader(DatabaseReader, AggregatorReader):
    """
    Reader mix from database and aggregator.
    """
    pass