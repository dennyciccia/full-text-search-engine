import os
import shutil
from whoosh.fields import Schema, ID, TEXT
from whoosh import index
import pandas as pd
import preprocessing as pp




# input: i documenti, cartella in cui verrà salvato l'index
def build_inverted_index(documents, index_dir):
    # definizione schema index
    schema = Schema(doc_id=ID(unique=True,stored=True),content=TEXT)

    # creazione indice (eliminazione di un eventuale index precedente)
    shutil.rmtree(index_dir)
    os.makedirs(index_dir)
    index.create_in(index_dir, schema)

    # apertura dell'indice e ottenimento del writer
    ix = index.open_dir(index_dir)
    writer = ix.writer()

    # aggiunta dei documenti all'indice
    for doc_id,text in documents:
        terms = pp.preprocess_document(text)
        if len(terms) > 0:
            writer.add_document(doc_id=str(doc_id),content="".join(terms))

    # commit delle modifiche all'indice
    writer.commit()

    stampa_indice(index)

if __name__ == "__main__":
    df = pd.read_csv("docs/csgo.csv", header=0, sep=';')
    documents = [(row['id'], row['text']) for _, row in df.iterrows()]
    build_inverted_index(documents,"index")