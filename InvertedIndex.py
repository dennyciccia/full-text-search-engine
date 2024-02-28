import os
from whoosh.fields import Schema, ID, TEXT
from whoosh.index import exists_in, open_dir, create_in
from whoosh.qparser import QueryParser
import preprocessing as pp

class InvertedIndex:
    def __init__(self, index_dir):
        self.index_dir = index_dir
        self.schema = Schema(doc_id=ID(unique=True,stored=True),content=TEXT)
        self.index = None

    @property
    def exist(self):
        return exists_in(self.index_dir)

    def setup_index(self, documents):
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
        self.build_index(documents)

    def open_index(self):
        self.index = open_dir(self.index_dir)

    def build_index(self, documents):
        # creazione inverted index
        self.index = create_in(self.index_dir, self.schema)
        writer = self.index.writer()
        # indicizzazione documenti
        for doc_id, text in documents:
            terms = pp.preprocess_document(text)
            if len(terms) > 0:
                writer.add_document(doc_id=str(doc_id), content="".join(terms))
        # commit delle modifiche all'indice
        writer.commit()

    def search_documents(self, search):
        with self.index.searcher() as searcher:
            query = QueryParser("content", self.index.schema).parse(search)
            results = searcher.search(query)
            return [dict(result) for result in results]