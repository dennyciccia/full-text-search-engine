# Search engine full-text
Progetto per l'esame di Gestione dell'informazione.

Search engine che permette di eseguire ricerche full-text su una collection di documenti.

--------------------------

**Query language**

query = ( content [, sentiment] | sentiment [, content] ) [, limit] [, mode]

content = content: _word_ _word_ ...

sentiment = sentiment: "anger"|"disgust"|"fear"|"joy"|"neutral"|"sadness"|"surprise"

limit = limit: _number_

mode = mode: (AND|OR)

operatore logico default: AND

limite di default: 10

--------------------------

**Installazione requisiti**

pip insall -r requirements.txt