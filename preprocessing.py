import nltk
import re

# inizializzazione
STEMMING = True
LEMMATIZATION = not STEMMING

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

stop_words = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.SnowballStemmer("english")
lemmatizer = nltk.WordNetLemmatizer()


# Converte Tag NLTK in Tag Wordnet
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return nltk.corpus.wordnet.NOUN


# creazione della sequenza di token per il testo passato come argomento
def preprocess_document(text):
    # salta le recensioni vuote
    if not isinstance(text, float):
        # Rende minuscolo
        text = text.lower()
        # Rimuove URL
        text = re.sub(r'http\S+', '', text)
        # Rimuove menzioni e hashtag
        text = re.sub(r'@\w+|#\w+', '', text)
        # Rimuove simboli inutili
        text = re.sub(r'[^a-z0-9 ]+', '', text)

        # Conversione del testo in token
        text_tokens = nltk.word_tokenize(text)

        # Rimozione delle stopwords e parole composte da una lettera
        filtered_tokens = [token for token in text_tokens if token not in stop_words and len(token) > 1]

        # Stemming
        if STEMMING:
            filtered_tokens = [stemmer.stem(token) for token in filtered_tokens]

        # Lemmatization
        if LEMMATIZATION:
            pos_tags = nltk.pos_tag(filtered_tokens)
            filtered_tokens = [lemmatizer.lemmatize(t[0], get_wordnet_pos(t[1])) for t in pos_tags]

        return filtered_tokens
    else:
        return []
