import os
from gensim.models import Word2Vec
import pandas as pd
from InvertedIndex import InvertedIndex
import preprocessing as pp

DOC_PATH = '../docs/BG3_reviews.csv'
WORD2VEC_MODEL_PATH = '../data/word2vec.model'
INDEX_DIR = '../data/index'


def get_documents():
    df = pd.read_csv(DOC_PATH, header=0, sep=';')
    documents = []
    for _, row in df.iterrows():
        cleaned_review = pp.preprocess_document(row['review'])
        documents.append((row['id'], cleaned_review, row['review'], row['timestamp_created'],
                          row['timestamp_updated'], row['voted_up'], row['votes_up'], row['votes_funny'],
                          row['written_during_early_access'], row['steam_purchase'], row['received_for_free']))
    return documents


def init_index_and_word2vec(force=False):
    index = InvertedIndex(INDEX_DIR)
    word2vec_model = None
    if os.path.exists(WORD2VEC_MODEL_PATH):
        word2vec_model = Word2Vec.load(WORD2VEC_MODEL_PATH)

    if force or not index.exists or word2vec_model is None:
        documents = get_documents()
        if force or not index.exists:
            print("Costruzione inverted index...")
            index.setup_index(documents)
        if force or word2vec_model is None:
            print("Addestramento modello word2vec...")
            word2vec_model = Word2Vec([d[1] for d in documents])
            word2vec_model.save(WORD2VEC_MODEL_PATH)

    return index, word2vec_model