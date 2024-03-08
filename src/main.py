import preprocessing as pp
import setup


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
        print(f"Testo recensione: {r['review'].strip()}")
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
            setup.init_index_and_word2vec(force=True)
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
            query = word2vec_expansion(input("Inserisci la query di ricerca: "))
            results = index.search_documents(content=query, limit=reviews_limit)
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


def query_language_menu():
    results = None
    repeat = True
    while repeat:
        try:
            input_query = input("Inserisci la query di ricerca: ")
            query = dict((k.strip(), v.strip()) for k, v in (element.split(': ') for element in input_query.split(', ')))

            query['content'] = pp.preprocess_document(query['content'])
            if query['word2vec'] == 'True':
                query['content'] = word2vec_expansion(query['content'])

            results = index.search_documents(**query)
        except (TypeError, ValueError):
            print("Query non valida")
        else:
            repeat = False
    print_results(results)


def word2vec_expansion(query):
    expanded_query = []
    for word in query:
        try:
            similar_words = word2vec_model.wv.most_similar(word, topn=3)
            expanded_query.extend([similar_word for similar_word, _ in similar_words])
        except KeyError:
            # se la parola non è nel vocabolario
            expanded_query.append(word)
    return expanded_query


if __name__ == "__main__":
    # inizializzazione indice e modello word2vec
    index, word2vec_model = setup.init_index_and_word2vec()

    # menu principale
    menu(index, word2vec_model)
