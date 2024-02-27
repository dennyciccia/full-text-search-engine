import nltk
import pandas as pd
import re

"""
text = "This is an english text, it is used as an example of the text that will be taken from the files (I think" \
        "CSV file), because now I don't have the document collection so for now it's ok."
"""

# Converte Tag NLTK in Tag Wordnet
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

# inizializzazione
STEMMING = True
LEMMATIZATION = not STEMMING

nltk.download("punkt")
nltk.download("stopwords")
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

docs_path = ["docs/elden_ring.csv"] #,"docs/csgo.csv"]
stop_words = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.SnowballStemmer("english")
lemmatizer = nltk.WordNetLemmatizer()

tokens = []

# creazione della sequenza di token per ogni file contenente le recensioni
for file in docs_path:
    df = pd.read_csv(file, header=0, sep=';')

    for rev in df["review"]:
        # salta le recensioni vuote
        if isinstance(rev,float):
            continue

        #conversione del testo in token
        rev_tokens = nltk.word_tokenize(rev.lower())

        # Rimozione delle stopwords e parole composte da una lettera
        filtered_tokens = [ token for token in rev_tokens if token not in stop_words and len(token) > 1 ]

        # Stemming
        if STEMMING:
            filtered_tokens = [ stemmer.stem(token) for token in filtered_tokens ]

        # Lemmatization
        if LEMMATIZATION:
            pos_tags = nltk.pos_tag(filtered_tokens)
            filtered_tokens = [ lemmatizer.lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags ]

        tokens.append(filtered_tokens)

print(tokens)