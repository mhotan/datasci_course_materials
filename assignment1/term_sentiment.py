import os
import sys
import json


def process_word(word):
    word = "".join(c for c in word if c not in ('!', '.', ':', ',', '?', '"', '(', ')', ';', '\'')).strip().lower()
    if word.startswith("#"):
        word.replace("#", '')
    return word

# Given an array of Strings processes all the words replaces the word with the processed word
def process_words(words, sentiment, associated_scores):
    for word in words:
        # filter word or phrases removing punctuations, Quotations symbols.
        # Remove extra characters
        word = process_word(word)
        if len(word) == 0 or word.find('@') != -1:
            continue
        if not word in associated_scores:
            associated_scores[word] = []
        associated_scores[word].append(sentiment)

# Calculate the Sentiment of a given term.
def calculate_sentiment(word, associated_scores):
    word = process_word(word)
    pos = 0
    neg = 0
    scores = associated_scores[word]
    for score in scores:
        if score > 0:
            pos += score
        elif score < 0:
            neg += abs(score)

    # If the score is the same assign the score of "word" to 0
    if pos == neg:
        return 0
    elif pos == 0:
        return neg
    elif neg == 0:
        return pos
    else:
        x = float(pos) / float(neg)
        if x >= 1:
            return x
        return -1.0 / x  # invert the fraction


def get_num(value):
    try:
        return int(value)
    except ValueError:
        return 0


def main():
    if not (len(sys.argv) == 2 or len(sys.argv) == 3):
        raise ValueError('Incorrect argument signature\n Correct signature: '
                         'frequency.py <sentiment_file> <tweet_file>')
    sentiment_file_path = sys.argv[1]
    if not os.path.isfile(sentiment_file_path):
        raise ValueError('Sentiment argument is not a file')
    tweet_file_path = sys.argv[2]
    if not os.path.isfile(tweet_file_path):
        raise ValueError('Tweet file Argument is not a file')
    tweet_file = open(tweet_file_path)  # The first file will should have all the tweets per line
    sentiment_file = open(sentiment_file_path)

    sentiments = []
    for line in sentiment_file.readlines():
        sentiments.append(get_num(line.strip()))

    associated_scores = {}

    lines = tweet_file.readlines()
     # Iterate through each JSON Object
    for idx in range(len(lines)):
        tweet = json.loads(lines[idx])
        # Extract the text field from the JSON Object
        if 'text' not in tweet:  # If there is no text then ignore this tweet.
            continue

        # Extract the tweet text from the JSON object.
        text = tweet['text']

        # Separate the words in the text.
        words = text.split(" ")
        process_words(words, sentiments[idx], associated_scores)

    # Close the files for the tweets
    tweet_file.close()
    sentiment_file.close()

    for word in associated_scores:
        if type(word) is unicode:
            print "{0} {1}".format(word.encode('utf-8'), str(calculate_sentiment(word, associated_scores)))
        else:
            print "{0} {1}".format(word, str(calculate_sentiment(word, associated_scores)))


if __name__ == '__main__':
    main()
