import os
from gensim.models import Word2Vec
import preprocessing as pp
import setup
from InvertedIndex import InvertedIndex
from config import INDEX_DIR, WORD2VEC_MODEL_PATH

index = None
word2vec_model = None

reviews_limit = 10


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
        print("Testo recensione: ", r['review'].replace('\n', ' '))
        print()


def menu():
    scelta = -1
    global reviews_limit
    while scelta != '0':
        print("1. Ricostruisci l'indice e modello Word2Vec - ATTENZIONE: operazione molto lenta!")
        print("2. Ricerca recensioni guidata")
        print("3. Ricerca recensioni con query language")
        print("0. Esci")
        scelta = input("Inserisci la tua scelta: ")

        if scelta == '1':
            setup.init_index_and_word2vec(index, word2vec_model, WORD2VEC_MODEL_PATH, force=True)
        elif scelta == '2':
            search_menu()
        elif scelta == '3':
            query_language_menu()
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
        print("4. Ricerca per testo con Word2Vec")
        print("5. Cambia limite di risultati (attuale: " + str(reviews_limit) + ")")
        print("0. Torna al menu principale")
        scelta = input("Inserisci la tua scelta: ")

        if scelta == '1':
            query = pp.preprocess_document(input("Inserisci la query di ricerca: "))
            results = index.search_documents(content=query, limit=reviews_limit)
            print_results(results)

        elif scelta == '2':
            results = index.search_documents(sentiment=sentiment_menu(), limit=reviews_limit)
            print_results(results)

        elif scelta == '3':
            query = pp.preprocess_document(input("Inserisci la query di ricerca: "))
            results = index.search_documents(content=query, sentiment=sentiment_menu(), limit=reviews_limit)
            print_results(results)

        elif scelta == '4':
            query = word2vec_expansion(pp.preprocess_document(input("Inserisci la query di ricerca: ")))
            results = index.search_documents(content=query, limit=reviews_limit, mode='OR')
            print_results(results)

        elif scelta == '5':
            reviews_limit = int(input("Inserisci il nuovo limite di risultati: "))
            print("Limite impostato a " + str(reviews_limit))

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


def check_query_language(content=None, sentiment=None, limit=10, mode='AND', word2vec=None, **kwargs):
    if content is None and sentiment is None:
        raise ValueError("Deve essere presente o il content o il sentiment")
    if sentiment is not None and not set(sentiment.split()).issubset({'anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise'}):
        raise ValueError("Sentiment non valido")
    if mode is not None and mode not in ['AND', 'OR']:
        raise ValueError("Mode deve essere 'AND' o 'OR'")
    if not isinstance(int(limit), int) or int(limit) <= 0:
        raise ValueError("Limit deve essere un intero positivo")
    if word2vec is not None:
        if word2vec not in ['True', 'False']:
            raise ValueError("Word2Vec deve essere True o False")
        if word2vec and content is None:
            raise ValueError("Se word2vec è True, content deve essere presente")
    if kwargs:
        raise ValueError("Parametri non validi")


def query_language_menu():
    results = None
    repeat = True
    while repeat:
        try:
            input_query = input("Inserisci la query di ricerca: ")
            query = dict(
                (k.strip(), v.strip()) for k, v in (element.split(': ') for element in input_query.split(', ')))

            check_query_language(**query)

            query['content'] = pp.preprocess_document(query['content'])
            if 'word2vec' in query.keys() :
                if query['word2vec'] == 'True':
                    query['content'] = word2vec_expansion(query['content'])
                    query['mode'] = 'OR'
                del query['word2vec']
            results = index.search_documents(**query)
        except (TypeError, ValueError) as e:
            print("Query non valida:", e)
        else:
            repeat = False
    print_results(results)


def word2vec_expansion(query):
    expanded_query = []
    for word in query:
        try:
            similar_words = word2vec_model.wv.most_similar(word, topn=3)
            expanded_query.extend([similar_word for similar_word, _ in similar_words])
            expanded_query.append(word)
        except KeyError:
            # se la parola non è nel vocabolario
            expanded_query.append(word)
    return expanded_query


if __name__ == "__main__":
    # inizializzazione indice e modello word2vec
    index = InvertedIndex(INDEX_DIR)
    if os.path.exists(WORD2VEC_MODEL_PATH):
        word2vec_model = Word2Vec.load(WORD2VEC_MODEL_PATH)

    setup.init_index_and_word2vec(index, word2vec_model, WORD2VEC_MODEL_PATH)
    index.open_index()

    # menu principale
    menu()
