import os

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

DOC_PATH = os.path.join(CONFIG_DIR, 'docs')
WORD2VEC_MODEL_PATH = os.path.join(CONFIG_DIR, 'data', 'word2vec.model')
INDEX_DIR = os.path.join(CONFIG_DIR, 'data', 'index')