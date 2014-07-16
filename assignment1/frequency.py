import codecs
import json
import os
import sys

__author__ = 'mhotan'

def process_word(word):
    word = "".join(c for c in word if c not in ('!', '.', ':', ',', '?', '"', '(', ')', ';', '\'')).strip().lower()
    if word.startswith("#"):
        word.replace("#", '')
    return word

# Given an array of Strings processes all the words replaces the word with the processed word
def process_words(words):
    words = words.split(' ')
    proc_words = []
    for word in words:
        # filter word or phrases removing punctuations, Quotations symbols.
        # add the sentiment score of the word to the ongoing SUM
        # Remove extra characters
        word = process_word(word)
        if len(word) == 0 or word.find('@') != -1:
            continue
        proc_words.append(word.lower())
    return proc_words


def count_words(words, word_counts):
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

def calc_frequencies(word_counts):
    total_words = 0
    for word in word_counts:
        total_words += word_counts[word]
    frequencies = {}
    for word in word_counts:
        frequencies[word] = float(word_counts[word]) / float(total_words)
    return frequencies

# Main method that validates script parameters.
def main():
    if len(sys.argv) != 2:
        raise ValueError('Incorrect argument signature\n Correct signature: '
                         'frequency.py <tweet_file>')
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        raise ValueError('Argument is not a file')
    tweet_file = open(file_path)  # The first file will should have all the tweets per line

    word_counts = {}
     # Iterate through each JSON Object
    for jsonObj in tweet_file.readlines():
        tweet = json.loads(jsonObj)
        # Extract the text field from the JSON Object
        if 'text' not in tweet:  # If there is no text then ignore this tweet.
            continue

        # Extract the tweet text from the JSON object.
        text = tweet['text']
        # Separate the words in the text.
        words = process_words(text)
        count_words(words, word_counts)
    frequencies = calc_frequencies(word_counts)
    for word in frequencies:
        if type(word) is unicode:
            print "{0} {1}".format(word.encode('utf-8'), str(frequencies[word]))
        else:
            print "{0} {1}".format(word, str(frequencies[word]))

if __name__ == '__main__':
    main()