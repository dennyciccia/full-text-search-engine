import os
from whoosh.fields import Schema, ID, TEXT
from whoosh.index import exists_in, open_dir, create_in
from whoosh.qparser import QueryParser
import preprocessing as pp

class InvertedIndex:
    def __init__(self, index_dir):
        self.__index_dir = index_dir
        self.__schema = Schema(doc_id=ID(unique=True, stored=True), content=TEXT)
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
        for doc_id, text in documents:
            terms = pp.preprocess_document(text)
            if len(terms) > 0:
                writer.add_document(doc_id=str(doc_id), content="".join(terms))
        # commit delle modifiche all'indice
        writer.commit()

    def search_documents(self, search):
        with self.__index.searcher() as searcher:
            query = QueryParser("content", self.__index.schema).parse(search)
            results = searcher.search(query)
            return [dict(result) for result in results]