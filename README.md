# Search engine full-text
Progetto per l'esame di Gestione dell'informazione.

## Informazioni

Search engine che permette di eseguire ricerche full-text su una collection di documenti.
La collezione di documenti è composta da oltre 300.000 recensioni di Steam di Baldur's Gate 3.

## Funzionalità

* Ricerca full-text su un corpus di documenti
* Filtraggio per sentiment (rabbia, disgusto, paura, gioia, neutralità, tristezza, sorpresa)
* Modalità di ricerca AND / OR
* Limite di risultati
* Opzione di utilizzare word2vec per la similarità semantica
* Ricerca di frasi esatte

## Query language

Le query sono composte da parametri:

* `content`: specifica le parole da cercare (opzionale, obbligatorio se non è presente `sentiment`),
   per usare l'operatore AND si usano && (default) e per l'operatore OR si usano || (con le parentesi si possono creare query complesse
    ```
    content: word1 word2 (word3 || word4) && word5
    ```
* `sentiment`: filtra i risultati per il sentimento specificato (opzionale, obbligatorio se non è presente `content`, si possono cercare più sentiment in OR separandoli da spazio)
    ```
    sentiment: anger | disgust | fear | joy | neutral | sadness | surprise
    ```
* `limit`: limita il numero di risultati (opzionale, default: 10)
    ```
    limit: number
    ```
* `word2vec`: abilita l'utilizzo di word2vec per la similarità semantica (opzionale, default: False)
    ```
    word2vec: True | False
    ```

## Istruzioni per l'utilizzo

Per utilizzare il programma eseguire lo script 'src/main.py', la prima volta che si usa verrà costruito l'inverted index (ATTENZIONE: operazione molto lenta).
Una volta avviato e costruito l'index si possono effettuare ricerche in modo guidato o usando il query language.

Per effettuare i benchmark eseguire lo script 'benchmark/benchmark_script.py', verrà avviato prima il benchmark della Mean Average Precision e poi il benchmark del Discounted Cumultive Gain.
Tutti i risultati di benchmark vengono salvati su file .csv.

## Requisiti

I requisiti sono elencati nel file `requirements.txt`.

Per installarli eseguire il comando:

```
pip install -r requirements.txt
```
