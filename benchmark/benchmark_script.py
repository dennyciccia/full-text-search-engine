import math
import pandas as pd
from src.InvertedIndex import InvertedIndex
import src.preprocessing as pp
from src.word2vec import Word2Vec
from config import UIN_PATH, INDEX_DIR


def mean_average_precision(index, queries):
    print("-- Benchmark per Mean Average Precision --")

    average_precisions_list = []

    for i, q in enumerate(queries):
        print(f"-- Query {i + 1} --")
        print(f"UIN: {q['UIN']}")
        print(f"Query originale: {q['fullquery']}")
        print(f"Query preprocessta: {' '.join(q['query']['content'])}")
        A = index.search_documents(**q['query'])
        relevant_docs = 0
        precisions_list = []

        for j, doc in enumerate(A):
            print(f"\nDocumento {j + 1}:")
            print(f"ID: {doc['id']}")
            print("Testo: ", doc['review'].replace('\n', ' '))
            if input("Rilevante? (s/n): ") == 's':
                relevant_docs += 1
                precision = relevant_docs / (j + 1)
                precisions_list.append(precision)
                print(f"Precision: {precision}")

        average_precision = sum(precisions_list) / len(precisions_list) if len(precisions_list) != 0 else 0
        average_precisions_list.append(average_precision)
        print(f"Average precision per la query {i + 1}: {average_precision}")

    return sum(average_precisions_list) / len(average_precisions_list), average_precisions_list


def DCG(index, queries):
    print("-- Benchmark per Discounted Cumulative Gain --")

    dcg_list = []
    for q in queries:
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
        dcg = scores[0]
        print(f"DCG doc 1: {scores[0]}")
        for i, score in enumerate(scores[1:], 1):
            dcg_doc = score / math.log2(i + 1)
            dcg += dcg_doc
            print(f"DCG doc {i + 1}: {dcg_doc}")

        print(f"DCG totale: {dcg}")
        dcg_list.append(dcg)
    return dcg_list


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
        queries.append({'UIN': row['UIN'], 'fullquery': row['query'], 'query': query})

    sentiment_input = input("Calcolare il sentiment? (s/n): ") == 's'
    word2vec_input = input("Calcolare il word2vec? (s/n): ") == 's'

    word2vec = Word2Vec()

    for q in queries:
        if not sentiment_input:
            del q['query']['sentiment']
        if word2vec_input:
            q['query']['content'] = word2vec.expansion(q['query']['content'])

    map, avpr_list = mean_average_precision(index, queries)
    #dcg_list = DCG(index, queries)

    with open("benchmark_MAP.csv", 'a') as fd:
        print(f"sentiment: {sentiment_input}; word2vec: {word2vec_input}; MAP: {map}", file=fd)
        for ap in avpr_list:
            print(f"{avpr_list}", file=fd)
    """    
    with open("benchmark_DCG.csv", 'a') as fd:
        print(f"sentiment: {sentiment_input}; word2vec: {word2vec_input};", file=fd)
        for dcg in dcg_list:
            print(f"{dcg}", file=fd)
    """

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
