import nltk

# parte che prende le informazioni dai file e le mette in text

text = "This is an english text, it is used as an example of the text that will be taken from the files (I think" \
        "CSV file), because now I don't have the document collection so for now it's ok."

# creazione dei token
tokens = nltk.word_tokenize(text)
print(tokens)