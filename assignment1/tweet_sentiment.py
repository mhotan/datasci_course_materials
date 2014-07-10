import sys
import json

def build_scores_dictionary():
    afinn_file = open("AFINN-111.txt")
    scores = {}  # initialize an empty dictionary
    for line in afinn_file:
        term, score = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    # print scores.items()  # Print every (term, score) pair in the dictionary TODO Delete
    return scores

def lines(fp):
    print str(len(fp.readlines()))

def main():
    tweet_file = open(sys.argv[1])

    # Populate the Sentiment Library
    scores = build_scores_dictionary()

    # Iterate through each JSON Object
    for jsonObj in tweet_file.readlines():
        tweet = json.loads(jsonObj)
        # Extract the text field from the JSON Object
        if 'text' not in tweet:  # If there is no text then ignore this tweet.
            continue

        text = tweet['text']
        print text + "\n"

        # Separate the words in the text.

    # Possibly filter word or phrases removing punctuations, Quotations symbols.
    # add the sentiment score of the word to the ongoing SUM

    # lines(tweet_file)

if __name__ == '__main__':
    main()
