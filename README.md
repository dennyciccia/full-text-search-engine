# Search engine full-text
Progetto per l'esame di Gestione dell'informazione.

Search engine che permette di eseguire ricerche full-text su una collection di documenti.

--------------------------

**Query language**

query -> content, sentiment, mode, limit

content = content: _word_ _word_ ...

sentiment = sentiment: "anger" | "disgust" | "fear" | "joy" | "neutral" | "sadness" | "surprise"

limit = limit: _number_

mode = mode: AND|OR

operatore logico default: AND

limite di default: 10

Devono essere sempre presenti content o sentiment, mode e limit sono opzionali.

--------------------------

**Installazione requisiti**

pip insall -r requirements.txt