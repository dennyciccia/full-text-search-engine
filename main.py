import pandas as pd
from InvertedIndex import InvertedIndex

INDEX_DIR = 'index'
DOC_PATH = 'docs/csgo.csv'

if __name__ == "__main__":
    index = InvertedIndex(INDEX_DIR)
    if not index.exists:
        print("Costruzione inverted index...")
        df = pd.read_csv(DOC_PATH, header=0, sep=';')
        documents = [(row['id'], row['text']) for _, row in df.iterrows()]
        index.setup_index(documents)
    else:
        index.open_index()

    query = input("Inserisci la tua query di ricerca: ")
    results = index.search_documents(query)
    for result in results:
        print(result)

