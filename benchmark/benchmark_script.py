import pandas as pd
from src.InvertedIndex import InvertedIndex

UIN_PATH = "UIN.csv"
INDEX_DIR = "../data/index"

def mean_average_precision(index, queries):
    pass

def DCG(index, queries):
    for q in queries:
        # esecuzione query
        query = dict((k.strip(), v.strip()) for k, v in (element.split(': ') for element in q.split(', ')))
        results = index.search_documents(**query)

        # mostra 1 risultato alla volta
            # chiede il punteggio


def R_qualcosa(index, queries):
    # array dei documenti rilevanti di tutte le query
    Ra_tot = []

    # esecuzione delle query e registrazione dei risultati
    for q, R in queries:
        query = dict((k.strip(), v.strip()) for k, v in (element.split(': ') for element in q.split(', ')))
        A = index.search_documents(**query)

        # documenti rilevanti trovati
        Ra = []
        for doc in A:
            if doc in R:
                Ra.append(doc)

        Ra_tot.append(Ra)

        # da finire ...

def do_benchmark():
    # apertura inverted index
    index = InvertedIndex(INDEX_DIR)
    index.open_index()

    # lettura delle query dal file
    # queries è una lista di tuple, ogni tupla ha la query in forma di stringa e una lista di id dei documenti rilevanti
    df = pd.read_csv(UIN_PATH, header=0, sep=';')
    queries = []
    for _, row in df.iterrows():
        queries.append((row['query'], row['R']))

    DCG(index, queries)



if __name__ == "__main__":
    do_benchmark()

# misure che hanno bisogno di R:
# - recall e precision
# - precision at seen relevant documents
# - F-measure (harmonic mean)
# - E-measure
# misure che non hanno bisogno di R:
# - average precision e mean average precision
# - DCG
