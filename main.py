import pandas as pd
from InvertedIndex import InvertedIndex
import preprocessing as pp

INDEX_DIR = 'index'
DOC_PATH = 'docs/BG3_reviews.csv'

index = InvertedIndex(INDEX_DIR)
reviews_limit = 10

def open_index(force=False):
    # l'indice viene costruito solo se non è già presente nella sua cartella
    if not index.exists or force:
        print("Costruzione inverted index...")
        df = pd.read_csv(DOC_PATH, header=0, sep=';')
        documents = [(row['id'], row['review'], row['timestamp_created'], row['timestamp_updated'], row['voted_up'],
                      row['votes_up'], row['votes_funny'], row['written_during_early_access'], row['steam_purchase'],
                      row['received_for_free']) for _, row in df.iterrows()]
        index.setup_index(documents)
    else:
        index.open_index()


def print_results(res):
    print("\n-- Risultati --\n")
    for r in res:
        print(f"ID recensione: {r['id']}")
        print("Recensione positiva") if r['voted_up'] else print("Recensione negativa")
        print(f"Data e ora creazione: {r['created']}")
        print(f"Data e ora aggiornamento: {r['updated']}")
        print(f"Gioco ricevuto gratis: {'Sì' if r['received_for_free'] else 'No'}")
        print(f"Comprato da Steam: {'Sì' if r['steam_purchase'] else 'No'}")
        print(f"Scritta durante l'accesso anticipato: {'Sì' if r['written_during_early_access'] else 'No'}")
        print(f"Utenti che l'hanno trovata utile: {r['votes_up']}")
        print(f"Utenti che l'hanno trovata divertente: {r['votes_funny']}")
        print(f"Sentimento rilevato: {r['sentiment']}, score: {r['score_sentiment']}")
        print(f"Testo recensione: {r['review'].strip()}")
        print()
        
        
def menu():
    scelta = -1
    while scelta != '0':
        print("1. Ricostruisci l'indice - ATTENZIONE: operazione molto lenta!")
        print("2. Cerca recensioni")
        print("0. Esci")
        scelta = input("Inserisci la tua scelta: ")
        
        if scelta == '1':
            open_index(force=True)
        elif scelta == '2':
            search_menu()
        elif scelta == '0':
            pass
        else:
            print("Scelta non valida")
        

def search_menu():
    scelta = -1
    global reviews_limit
    while scelta != '0':
        print("1. Ricerca per testo")
        print("2. Ricerca per sentimento")
        print("3. Ricerca per testo e sentimento")
        print("4. Cambia limite di risultati (attuale: " + str(reviews_limit) + ")")
        print("0. Torna al menu principale")
        scelta = input("Inserisci la tua scelta: ")
        
        if scelta == '1':
            query = input("Inserisci la query di ricerca: ")
            query = ' '.join(pp.preprocess_document(query))
            results = index.search_documents(content=query, limit=reviews_limit)
            print_results(results)

        elif scelta == '2':
            results = index.search_documents(sentiment=sentiment_menu(), limit=reviews_limit)
            print_results(results)

        elif scelta == '3':
            query = input("Inserisci la query di ricerca: ")
            query = ' '.join(pp.preprocess_document(query))
            results = index.search_documents(content=query, sentiment=sentiment_menu(), limit=reviews_limit)
            print_results(results)

        elif scelta == '4':
            reviews_limit = int(input("Nuovo limite: "))

        elif scelta == '0':
            pass

        else:
            print("Scelta non valida")
        

def sentiment_menu():
    scelta = -1
    sentiment = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
    while scelta != '0':
        print("Scegli un sentimento da cercare:")
        print("1. Anger (Rabbia)")
        print("2. Disgust (Disgusto)")
        print("3. Fear (Paura)")
        print("4. Joy (Gioia)")
        print("5. Neutral (Neutro)")
        print("6. Sadness (Tristezza)")
        print("7. Surprise (Sorpresa)")
        print("0. Torna al menu principale")
        scelta = int(input("Inserisci la tua scelta: "))

        if scelta in range(1, 8):
            return sentiment[scelta - 1]
        elif scelta == 0:
            pass
        else:
            print("Scelta non valida")


def menu_libero():
    results = None
    repeat = True
    while repeat:
        try:
            input_query = input("Inserisci la query di ricerca: ")
            query = dict((k.strip(), v.strip()) for k,v in (element.split(': ') for element in input_query.split(', ')))
            results = index.search_documents(**query)
        except (TypeError, ValueError):
            print("Query non valida")
        else:
            repeat = False
    print_results(results)


if __name__ == "__main__":
    # definizione e costruzione inverted index
    open_index()

    # fase di searching
    scelta = -1
    while scelta != '0':
        print("1. Ricerca guidata")
        print("2. Ricerca con query language")
        print("0. Esci")
        scelta = input("Scelta: ")
        if scelta == '1':
            menu()
        elif scelta == '2':
            menu_libero()