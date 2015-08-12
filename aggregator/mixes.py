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
    def __init__(self, **kwargs):
        "Base init."
        super(MixedLink, self).__init__(**kwargs)
        self._pickers = None

    @property
    def pickers(self):
        "Sorted link readers."
        pickers = {int(picker_id): picker_moment for \
            picker_id, picker_moment in self.get_pickers(withscores=True)}
        readers = MixedReader.query.filter(MixedReader.id.in_(pickers.keys())).all()
        for reader in readers:
            reader.moment = pickers[reader.id]
        readers.sort(key=attrgetter('moment'), reverse=True)
        self._pickers = readers
        return self._pickers


class MixedReader(DatabaseReader, AggregatorReader):
    """
    Reader mix from database and aggregator.
    Retrieve from database and sort aggregated data (i.e. fellows, edition)
    """
    def __init__(self, **kwargs):
        "Base init."
        super(MixedReader, self).__init__(**kwargs)
        self.init()

    def init(self):
        self._picks = None
        self._fellows = None
        self._edition = None

    def load(self):
        "Load details from database."
        self.init()

        # Fellows
        fellows = {int(fellow_id): fellow_fellowship for \
            fellow_id, fellow_fellowship in self.get_fellows(withscores=True)}
        if fellows:
            readers = MixedReader.query.filter(MixedReader.id.in_(fellows.keys())).all()
            for reader in readers:
                reader.fellowship = fellows[reader.id]
            readers.sort(key=attrgetter('fellowship'), reverse=True)
        else:
            readers = []
        self._fellows = readers
        fellows = self._fellows
        fellows_dict = {f.id: f for f in fellows}

        # Picks
        picks = {int(link_id): link_moment for \
            link_id, link_moment in self.get_picks(withscores=True)}
        links = MixedLink.query.filter(MixedLink.id.in_(picks.keys())).all()
        for link in links:
            link.moment = picks[link.id]
        links.sort(key=attrgetter('moment'), reverse=True)
        for link in links:
            pickers_ids = set(int(picker_id) for picker_id in link.get_pickers())
            link_fellows = [fellows_dict[fid] for \
                fid in pickers_ids.intersection(fellows_dict)]
            link_fellows.sort(key=attrgetter('fellowship'), reverse=True)
            link.fellows = [self] + link_fellows
        self._picks = links

        # Edition
        edition_fellows = self.get_edition_fellows()
        edition = {int(news_id): (news_relevance, \
            [int(fellow_id) for fellow_id in edition_fellows[news_id].split(',')]) \
            for news_id, news_relevance in self.get_edition(withscores=True)}
        if edition:
            links = MixedLink.query.filter(MixedLink.id.in_(edition.keys())).all()
            for link in links:
                link.relevance, link.fellows_ids = edition[link.id]
            links.sort(key=attrgetter('relevance'), reverse=True)
            for link in links:
                link_fellows = [fellows_dict[fid] for fid in link.fellows_ids]
                link_fellows.sort(key=attrgetter('fellowship'), reverse=True)
                link.fellows = link_fellows
        else:
            links = []
        self._edition = links

    ## Loaded properties
    @property
    def picks(self):
        "Sorted picked links."
        return self._picks

    @property
    def fellows(self):
        "Sorted fellow readers."
        return self._fellows

    @property
    def edition(self):
        "Sorted edition links."
        return self._edition
