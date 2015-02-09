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

    @property
    def markers(self):
        "Query on link markers."
        ids = self.get_markers()
        return MixedReader.query.filter(MixedReader.id.in_(ids))


class MixedReader(DatabaseReader, AggregatorReader):
    """
    Reader mix from database and aggregator.
    Define database queries for aggregated details (e.g.: fellows)
    """

    @property
    def fellows(self):
        "Query on fellow readers."
        ids = self.get_fellows()
        return MixedReader.query.filter(MixedReader.id.in_(ids))

    @property
    def edition(self):
        "Query on edition links."
        ids = self.get_edition()
        return MixedLink.query.filter(MixedLink.id.in_(ids))
