from config import WORD2VEC_MODEL_PATH
from gensim.models import Word2Vec as W2V


class Word2Vec:
    def __init__(self):
        self.model = W2V.load(WORD2VEC_MODEL_PATH)

    def expansion(self, query):
        expanded_query = []
        for word in query:
            try:
                similar_words = self.model.wv.most_similar(word, topn=1)
                expanded_query.extend(['(', word, 'OR', similar_words[0][0], ')'])
            except KeyError:
                # se la parola non è nel vocabolario
                expanded_query.append(word)
        return expanded_query
