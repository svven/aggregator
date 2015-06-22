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
    def pickers(self):
        "Sorted link readers."
        pickers = {picker_id: picker_moment for \
            picker_id, picker_moment in self.get_pickers(withscores=True)}
        readers = MixedReader.query.filter(MixedReader.id.in_(pickers.keys())).all()
        for reader in readers:
            reader.moment = pickers[str(reader.id)]
        readers.sort(key=attrgetter('moment'), reverse=True)
        return readers


class MixedReader(DatabaseReader, AggregatorReader):
    """
    Reader mix from database and aggregator.
    Retrieve from database and sort aggregated data (i.e. fellows, edition)
    """

    @property
    def picks(self):
        "Sorted picked links."
        picks = {link_id: link_moment for \
            link_id, link_moment in self.get_picks(withscores=True)}
        links = MixedLink.query.filter(MixedLink.id.in_(picks.keys())).all()
        for link in links:
            link.moment = picks[str(link.id)]
        links.sort(key=attrgetter('moment'), reverse=True)
        return links


    @property
    def fellows(self):
        "Sorted fellow readers."
        fellows = {fellow_id: fellow_fellowship for \
            fellow_id, fellow_fellowship in self.get_fellows(withscores=True)}
        if not fellows:
            return []
        readers = MixedReader.query.filter(MixedReader.id.in_(fellows.keys())).all()
        for reader in readers:
            reader.fellowship = fellows[str(reader.id)]
        readers.sort(key=attrgetter('fellowship'), reverse=True)
        return readers

    @property
    def edition(self):
        "Sorted edition links."
        fellows = set(self.get_fellows()) # redundant 

        edition = {news_id: (news_relevance, \
            set.intersection(set(AggregatorLink(news_id).get_pickers()), fellows)) \
            for news_id, news_relevance in self.get_edition(withscores=True)}

        # edition = {}
        # no_links_by_fellows = {} # {'fid1,fid2':no_links}
        # for link_id, link_relevance in \
        #     self.get_edition(count=config.NEWS_LIMIT, withscores=True):
        #     pickers = set(AggregatorLink(link_id).get_pickers())
        #     link_fellows = sorted(set.intersection(fellows, pickers))
        #     key = ','.join(link_fellows)
        #     no_links = no_links_by_fellows.get(key, 0) + 1
        #     if no_links > 3:
        #         continue
        #     else:
        #         no_links_by_fellows[key] = no_links
        #     edition[link_id] = (link_relevance, link_fellows)
        #     if len(edition) >= config.NEWS_COUNT:
        #         break

        if not edition:
            return []
        links = MixedLink.query.filter(MixedLink.id.in_(edition.keys())).all()
        for link in links:
            link.relevance, link.fellows_ids = edition[str(link.id)]
        links.sort(key=attrgetter('relevance'), reverse=True)
        return links




