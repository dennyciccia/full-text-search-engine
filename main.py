import pandas as pd
from InvertedIndex import InvertedIndex
import preprocessing as pp

INDEX_DIR = 'index'
DOC_PATH = 'docs/BG3_reviews.csv'


def print_results(res):
    print("\n-- Risultati --\n")
    for r in res:
        print(f"ID recensione: {r['id']}")
        print("Recensione positiva") if r['voted_up'] else print("Recensione negativa")
        print(f"Data e ora creazione: {r['created']}")
        print(f"Data e ora aggiornamento: {r['updated']}")
        print(f"Gioco ricevuto gratis: {r['received_for_free']}")
        print(f"Comprato da steam: {r['steam_purchase']}")
        print(f"Scritta durante l'accesso anticipato: {r['written_during_early_access']}")
        print(f"Utenti che l'hanno trovata utile: {r['votes_up']}")
        print(f"Utenti che l'hanno trovata divertente: {r['votes_funny']}")
        print(f"Testo recensione: {r['review'].strip()}")
        print()


if __name__ == "__main__":
    index = InvertedIndex(INDEX_DIR)
    # l'indice viene costruito solo se non è già presente nella sua cartella
    if not index.exists:
        print("Costruzione inverted index...")
        df = pd.read_csv(DOC_PATH, header=0, sep=';')
        documents = [(row['id'], row['review'], row['timestamp_created'], row['timestamp_updated'], row['voted_up'],
                      row['votes_up'], row['votes_funny'], row['written_during_early_access'], row['steam_purchase'],
                      row['received_for_free']) for _, row in df.iterrows()]
        index.setup_index(documents)
    else:
        index.open_index()

    # fase di searching
    query = input("Inserisci la query di ricerca: ")
    query = ' '.join(pp.preprocess_document(query))
    results = index.search_documents(query)
    print_results(results)
