import os
import sys
import json
import twitter_query as tq

scores = {}

def build_scores_dictionary():
    afinn_file = open("AFINN-111.txt")
     # initialize an empty dictionary
    for line in afinn_file:
        term, score = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

# Given an array of Strings processes all the words replaces the word with the processed word
def process_words(words):
    proc_words = []
    for word in words:
        word = word.strip() # Remove trailing and preceeding white spaces.
        word = "".join(c for c in word if c not in ('!','.',':',',',';','(',')',"\""))  # Remove common punctuations and quotes
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


def calculate_sentiments(array_of_tweets):
    sentiments = []
    for tweet in array_of_tweets:
        # Extract the text field from the JSON Object
        if 'text' not in tweet:  # If there is no text then ignore this tweet.
            continue

        # Extract the tweet text from the JSON object.
        text = tweet['text']
        # Separate the words in the text.
        words = text.split(" ")
        words = process_words(words)
        sentiments.append(calculate_sentiment(words))
    return sentiments

def main():
    #
    if not (len(sys.argv) == 2 or len(sys.argv) == 3):
        raise ValueError('Incorrect argument signature\n Correct signature: '
                         'frequency.py <url> <output_file>(Optional)')
    if len(sys.argv) == 3 and os.path.exists(sys.argv[2]) and not os.path.isfile(sys.argv[2]):
        raise ValueError('Output Argument is not a file')
    #
    try:
        os.remove(sys.argv[2])
    except OSError:
        pass

    # Populate the Sentiment Library
    build_scores_dictionary()

    lines = []
    jarray = tq.get_json_result(sys.argv[1])
    # Iterate through each JSON Object
    for sentiment_score in calculate_sentiments(jarray):
        lines.append(str(sentiment_score) + '\n')

    output = ''.join(lines)
    if len(sys.argv) == 2:
        print(output)
    else:
        output_file = open(sys.argv[2], 'w')
        output_file.write(output)
        output_file.close()

if __name__ == '__main__':
    main()
