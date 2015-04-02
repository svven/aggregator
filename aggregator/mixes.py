"""
Mixed models: Reader, Link
"""
from operator import attrgetter

import config
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
        "Sorted link markers."
        markers_ids = {mid[0]: mid[1] for mid in self.get_markers(withscores=True)}
        markers = MixedReader.query.filter(MixedReader.id.in_(markers_ids.keys())).all()
        for m in markers: m.moment = markers_ids[str(m.id)]
        markers.sort(key=attrgetter('moment'), reverse=True)
        return markers


class MixedReader(DatabaseReader, AggregatorReader):
    """
    Reader mix from database and aggregator.
    Retrieve from database and sort aggregated data (i.e. fellows, edition)
    """

    @property
    def fellows(self):
        "Sorted fellow readers."
        fellows_ids = {fid[0]: fid[1] for fid in self.get_fellows(withscores=True)}
        fellows = MixedReader.query.filter(MixedReader.id.in_(fellows_ids.keys())).all()
        for f in fellows: f.fellowship = fellows_ids[str(f.id)]
        fellows.sort(key=attrgetter('fellowship'), reverse=True)
        return fellows

    @property
    def edition(self):
        "Sorted edition links."
        edition_ids = {nid[0]: nid[1] for nid in self.get_edition(count=config.MARKS_LIMIT, withscores=True)}
        edition = MixedLink.query.filter(MixedLink.id.in_(edition_ids.keys())).all()
        for n in edition: n.relevance = edition_ids[str(n.id)]
        edition.sort(key=attrgetter('relevance'), reverse=True)
        return edition
