# Search engine full-text
Progetto per l'esame di Gestione dell'informazione.

## Informazioni

---------------------------------------

Search engine che permette di eseguire ricerche full-text su una collection di documenti.
La collezione di documenti è composta da oltre 300.000 recensioni di Steam di Baldur's Gate 3.

## Funzionalità

---------------------------------------

* Ricerca full-text su un corpus di documenti
* Filtraggio per sentiment (rabbia, disgusto, paura, gioia, neutralità, tristezza, sorpresa)
* Modalità di ricerca AND / OR
* Limite di risultati
* Opzione di utilizzare word2vec per la similarità semantica
* Ricerca di frasi esatte


## Query language

--------------------------

Le query sono composte da parametri:

* `content`: specifica le parole da cercare (opzionale, obbligatorio se non è presente `sentiment`)
    ```
    content: word1 word2 ...
    ```
  per cercare una frase esatta si possono mettere le parole tra doppi apici
  ```
    content: "phrase"
  ```
* `sentiment`: filtra i risultati per il sentimento specificato (opzionale, obbligatorio se non è presente `content`)
    ```
    sentiment: "anger" | "disgust" | "fear" | "joy" | "neutral" | "sadness" | "surprise"
    ```
* `mode`: specifica la modalità di ricerca (opzionale, default: AND)
    ```
    mode: AND | OR
    ```
* `limit`: limita il numero di risultati (opzionale, default: 10)
    ```
    limit: number
    ```
* `word2vec`: abilita l'utilizzo di word2vec per la similarità semantica (opzionale, default: False)
    ```
    word2vec: True | False
    ```
  
## Requisiti

--------------------------

I requisiti sono elencati nel file `requirements.txt`.

Per installarli eseguire il comando:

```
pip install -r requirements.txt
```