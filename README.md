# Search engine full-text
Progetto per l'esame di Gestione dell'informazione.

Search engine che permette di eseguire ricerche full-text su una collection di documenti.

--------------------------

**Query language**

query -> content, sentiment, mode, limit, word2vec

content = content: _word_ _word_ ...

sentiment = sentiment: "anger" | "disgust" | "fear" | "joy" | "neutral" | "sadness" | "surprise"

mode = mode: AND|OR

limit = limit: _number_

word2vec = word2vec: True|False

operatore logico default: AND

operatore logico per word2vec: OR

word2vec default: False

limite di default: 10

Devono essere sempre presenti content o sentiment, invece mode, limit e word2vec sono opzionali.

Si può cercare una frase esatta mettendo le parole tra doppi apici ("...").

--------------------------

**File requisiti**

requirements.txt