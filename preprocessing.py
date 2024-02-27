import nltk
from nltk.corpus import stopwords
import pandas as pd
import re

"""
text = "This is an english text, it is used as an example of the text that will be taken from the files (I think" \
        "CSV file), because now I don't have the document collection so for now it's ok."
"""

# inizializzazione
nltk.download("punkt")
nltk.download("stopwords")
docs_path = ["docs/elden_ring.csv", "docs/csgo.csv"]
stop_words = set(stopwords.words('english'))

tokens = []

for file in docs_path:
    df = pd.read_csv(file, header=0, sep=';')

    for rev in df["review"]:
        if isinstance(rev,float):
            continue

        #conversione del testo in token
        rev_tokens = nltk.word_tokenize(rev.lower())

        #rimozione delle stopwords e altri simboli non utili
        filtered_tokens = [token for token in rev_tokens if re.search("[a-z0-9]+",token) and token not in stop_words]

        tokens.append(filtered_tokens)

print(tokens)