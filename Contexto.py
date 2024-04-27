import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

import gensim.downloader as api
from gensim.models import KeyedVectors
import os

# Check if the model file exists
model_file = 'word2vec-google-news-300.model'
if os.path.isfile(model_file):
    # Load the model from disk
    vectorized_data = KeyedVectors.load(model_file)
else:
    # Load the model from the API if the file doesn't exist
    vectorized_data = api.load('word2vec-google-news-300')
    # Save the model to disk for future use
    vectorized_data.save(model_file)

example_sentence = "Living cannot be the human function because it is a function shared by other species.".replace(".","").replace(",","").replace("!","").replace("?","").split()
print(example_sentence)

tagged_sentence = nltk.pos_tag(example_sentence)

#
important_words = []
for word_tag in tagged_sentence:
    if word_tag[1][0] in ["V", "N"]:
        important_words.append((word_tag[0], vectorized_data.most_similar(word_tag[0], topn=1)))

print(important_words)