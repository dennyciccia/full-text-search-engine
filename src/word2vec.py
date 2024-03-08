from gensim.models import Word2Vec
import preprocessing as pp

reviews = [
    "I love this phone",
    "I hate spaghetti",
    "Everything was cold",
    "Everything was hot exactly as I wanted",
    "Everything was green",
    "the host seated us immediately",
    "they gave us free chocolate cake",
    "not good for business",
]

cleaned_reviews = [pp.preprocess_document(r) for r in reviews]


def init_word2vec_model(cleaned_reviews):
    return Word2Vec(cleaned_reviews, vector_size=100, window=5, min_count=1, workers=4)


model = init_word2vec_model(cleaned_reviews)
print(model)
