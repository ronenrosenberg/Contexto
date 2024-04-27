import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

import gensim.downloader as api
from gensim.models import KeyedVectors
import os

# Check if the model file exists
model_file = 'fasttext-wiki-news-subwords-300.model'
if os.path.isfile(model_file):
    print("a")
    # Load the model from disk
    vectorized_data = KeyedVectors.load(model_file)
else:
    print("b")
    # Load the model from the API if the file doesn't exist
    vectorized_data = api.load('fasttext-wiki-news-subwords-300')
    # Save the model to disk for future use
    vectorized_data.save(model_file)


example_sentence = "Thing.".replace(".","").replace(",","").replace("!","").replace("?","").split()

tagged_sentence = nltk.pos_tag(example_sentence)
#
important_words = []
#for all words in the sentence
for i in range(len(tagged_sentence)):
    #if word is a verb or nounj
    to_be_guessed = False
    if tagged_sentence[i][1][0] in ["V", "N"]:
        #create a list of similar words
        similar_list = vectorized_data.most_similar(tagged_sentence[i][0], topn=20)
        #make sure words in similar list are all lowercase and of same part of speech
        similar_list = [data[0].lower() for data in similar_list if nltk.pos_tag([data[0]])[0][1] == tagged_sentence[i][1] and tagged_sentence[i][0] != data[0].lower()]
        
        to_be_guessed = True
        #index to replace, original word, and similar word list
    important_words.append([to_be_guessed, [tagged_sentence[i][0].lower()] + similar_list])

print(important_words)

def print_and_underline():
    print_list = []
    for i in range(len(important_words)):
        #if is a word to be guessed and isn't already correct, underline it
        if important_words[i][0] and len(important_words[i][1]) > 1:
            if i == 0:
                print_list.append('\033[4m' + important_words[i][1][-1].capitalize().replace("_", " ") + '\033[0m')
            else:
                print_list.append('\033[4m' + important_words[i][1][-1].replace("_", " ") + '\033[0m')
        #else just print it
        else:
            if i == 0:  
                print_list.append(example_sentence[i].capitalize().replace("_", " "))
            else:
                print_list.append(example_sentence[i].replace("_", " "))

    #actual printing
    for i in range(len(print_list)):
        if i != len(print_list)-1: 
            print(print_list[i], end=' ')
        else:
            print(print_list[i], end='')
    print('.')

def check_if_better(user_guess):
    changed = False
    for word in important_words:
        if word[0]:
            if user_guess in word[1][:-1]:
                changed = True
                if word[1][:-1].index(user_guess) == 0:
                    word[1] = [user_guess]
                    print(f"You got it! \"{user_guess}\" was one of the missing words.")
                else:
                    new_index = word[1][:-1].index(user_guess)
                    word[2] = word[1][:new_index+1]
                    print(f"Nice! \"{user_guess}\" is {new_index} degrees of separation away from the actual word.")
    if not changed:
        print("Sorry, but that doesn't seem to be right.")
    print()

while True:
    print_and_underline()
    user_guess = input("Do you have a guess to improve the sentence? ")
    check_if_better(user_guess)
    
    end_condition = not [data[1] for data in important_words if data[0] and len(data[1]) > 1]
    if end_condition: 
        print("You figured out the sentence! You win!")
        break


