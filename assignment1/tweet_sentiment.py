import codecs
import os
import sys
import json

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

scores = {}

def process_word(word):
    word = "".join(c for c in word if c not in ('!', '.', ':', ',', '?', '"', '(', ')', ';', '\'')).strip().lower()
    if word.startswith("#"):
        word.replace("#", '')
    return word

def build_scores_dictionary(afinn_file):
    afinn_file = open(afinn_file)
     # initialize an empty dictionary
    for line in afinn_file:
        term, score = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.


# Given an array of Strings processes all the words replaces the word with the processed word
def process_words(words):
    proc_words = []
    for word in words:
        # Remove extra characters
        word = process_word(word)
        if len(word) == 0 or word.find('@') != -1:
            continue
        proc_words.append(word.lower())
    return proc_words


def calculate_sentiment(words):
    # Calculate the Sentiment.
    score = 0
    for word in words:
        if word in scores:
            score += scores[word]
    return score


def main():
    #
    if not (len(sys.argv) == 2 or len(sys.argv) == 3):
        raise ValueError('Incorrect argument signature\n Correct signature: '
                         'tweet_sentiment.py <AFINN file> <output_file>(Optional)')
    afinn_file = sys.argv[1]
    if not os.path.isfile(afinn_file):
        raise ValueError('AFINN argument is not a file')
    file_path = sys.argv[2]
    if not os.path.isfile(file_path):
        raise ValueError('Tweet inputs Argument is not a file')

    # Populate the Sentiment Library
    build_scores_dictionary(afinn_file)

    # Open file to read tweets
    tweet_file = open(file_path)
    tweet_lines = tweet_file.readlines()

    # Iterate through each JSON Object
    for jsonObj in tweet_lines:
        tweet = json.loads(jsonObj)
        # Extract the text field from the JSON Object
        if 'text' not in tweet:  # If there is no text then ignore this tweet.
            print "{0}".format(0)
            continue

        # Extract the tweet text from the JSON object.
        text = tweet['text']

        # Separate the words in the text.
        words = text.split(" ")
        words = process_words(words)
        print "{0}".format(calculate_sentiment(words))

    # Close the files for the tweets
    tweet_file.close()

if __name__ == '__main__':
    main()
