from transformers import pipeline

# Carica la pipeline di analisi del sentimento
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Esempio di testo da analizzare
testo = "50/50 game, it's a good game but it's not for all people"

# Esegui la sentiment analysis sul testo
risultato = classifier(testo)
print(risultato)