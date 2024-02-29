import os
from datetime import datetime
from whoosh.fields import Schema, ID, TEXT, DATETIME, BOOLEAN, NUMERIC
from whoosh.index import exists_in, open_dir, create_in
from whoosh.qparser import QueryParser
import preprocessing as pp

class InvertedIndex:
    def __init__(self, index_dir):
        self.__index_dir = index_dir
        self.__schema = Schema(
            id=ID(unique=True, stored=True),
            content=TEXT(stored=False),
            review=TEXT(stored=True),
            created=DATETIME(stored=True),
            updated=DATETIME(stored=True),
            voted_up=BOOLEAN(stored=True),
            votes_up=NUMERIC(stored=True),
            votes_funny=NUMERIC(stored=True),
            written_during_early_access=BOOLEAN(stored=True),
            steam_purchase=BOOLEAN(stored=True),
            received_for_free=BOOLEAN(stored=True)
        )
        self.__index = None

    @property
    def exists(self):
        return exists_in(self.__index_dir)

    def setup_index(self, documents):
        if not os.path.exists(self.__index_dir):
            os.mkdir(self.__index_dir)
        self.build_index(documents)

    def open_index(self):
        self.__index = open_dir(self.__index_dir)

    def build_index(self, documents):
        # creazione inverted index
        self.__index = create_in(self.__index_dir, self.__schema)
        writer = self.__index.writer()
        # indicizzazione documenti
        for id, review, created, updated, voted_up, votes_up, votes_funny, written_during_early_access, steam_purchase, received_for_free in documents:
            terms = pp.preprocess_document(review)
            if len(terms) > 0:
                writer.add_document(
                    id=str(id),
                    content=' '.join(terms),
                    review=review,
                    created=datetime.fromtimestamp(created),
                    updated=datetime.fromtimestamp(updated),
                    voted_up=voted_up,
                    votes_up=votes_up,
                    votes_funny=votes_funny,
                    written_during_early_access=written_during_early_access,
                    steam_purchase=steam_purchase,
                    received_for_free=received_for_free
                )
        # commit delle modifiche all'indice
        writer.commit()

    def search_documents(self, search):
        query = QueryParser("content", schema=self.__schema).parse(search)
        with self.__index.searcher() as searcher:
            results = searcher.search(query)
            return [dict(result) for result in results]
