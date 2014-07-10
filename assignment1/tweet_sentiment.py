import sys
import json

scores = {}

def build_scores_dictionary():
    afinn_file = open("AFINN-111.txt")
     # initialize an empty dictionary
    for line in afinn_file:
        term, score = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

def lines(fp):
    print str(len(fp.readlines()))

# Given an array of Strings processes all the words replaces the word with the processed word
def process_words(words):
    proc_words = []
    for word in words:
        word = word.strip() # Remove trailing and preceeding white spaces.
        word = "".join(c for c in word if c not in ('!','.',':',',',"\""))  # Remove common punctuations and quotes
        proc_words.append(word.lower())
    return proc_words

#
def calculate_sentiment(words):
    score = 0
    for word in words:
        if word in scores:
            score += scores[word]
    return score

def main():
    # Populate the Sentiment Library
    build_scores_dictionary()

    # Open file to read tweets
    tweet_file = open(sys.argv[1])

    # Iterate through each JSON Object
    for jsonObj in tweet_file.readlines():
        tweet = json.loads(jsonObj)
        # Extract the text field from the JSON Object
        if 'text' not in tweet:  # If there is no text then ignore this tweet.
            continue

        # Extract the tweet text from the JSON object.
        text = tweet['text']

        # Separate the words in the text.
        words = text.split(" ")
        words = process_words(words)
        print calculate_sentiment(words)

    # Possibly filter word or phrases removing punctuations, Quotations symbols.
    # add the sentiment score of the word to the ongoing SUM

    # lines(tweet_file)

if __name__ == '__main__':
    main()
