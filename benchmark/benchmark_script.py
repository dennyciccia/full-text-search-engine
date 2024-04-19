import math

import pandas as pd
from src.InvertedIndex import InvertedIndex
import src.preprocessing as pp

UIN_PATH = "UIN.csv"
INDEX_DIR = "../data/index"


def mean_average_precision(index, queries):
    average_precisions_list = []

    for i, q in enumerate(queries):
        print("Query " + str(i + 1) + ": ", ' '.join(q['query']["content"]))
        A = index.search_documents(**q['query'])
        relevant_docs = 0
        precisions_list = []

        for j, doc in enumerate(A):
            print("Documento " + str(j+1) + ": ", doc["review"])
            if input("Rilevante? (s/n): ") == 's':
                relevant_docs += 1
                precision = relevant_docs / (j + 1)
                precisions_list.append(precision)

        average_precision = sum(precisions_list) / len(precisions_list) if len(precisions_list) != 0 else 0
        average_precisions_list.append(average_precision)

    return sum(average_precisions_list) / len(average_precisions_list)


def DCG(index, queries):
    for q in queries:
        # esecuzione query
        del q['query']['sentiment']
        results = index.search_documents(**q['query'])
        scores = []

        print("\nQuery:", q['UIN'], end='\n\n')
        for doc in results:
            print("Review:", doc['review'].replace('\n', ' '))

            # inserimento del voto di rilevanza
            while True:
                try:
                    score = int(input("Inserisci il voto di rilevanza per il documento (0-3): "))
                    if 0 <= score <= 3:
                        scores.append(score)
                        print("")
                        break
                    else:
                        print("Errore: Il punteggio deve essere compreso tra 0 e 3.")
                except ValueError:
                    print("Errore: Per favore inserisci un numero intero.")

        # calcolo DCG
        dcg = 0
        for i, score in enumerate(scores, start=1):
            dcg_doc = (2 ** score - 1) / math.log(i + 1)
            dcg += dcg_doc
            print(f"DCG doc {i}: {dcg_doc}")

        print(f"DCG totale: {dcg}")


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
    # queries è una lista di dizionari
    df = pd.read_csv(UIN_PATH, header=0, sep=';')
    queries = []
    for _, row in df.iterrows():
        query = dict((k.strip(), v.strip()) for k, v in (element.split(': ') for element in row['query'].split(', ')))
        query['content'] = pp.preprocess_document(query['content'], is_query=True)
        queries.append({'UIN': row['UIN'], 'query': query})

    mean_average_precision(index, queries)
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
