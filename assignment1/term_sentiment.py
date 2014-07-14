import os
import sys
import json

associated_words = {}


def build_scores_dictionary():
    scores = {}
    afinn_file = open("AFINN-111.txt")
     # initialize an empty dictionary
    for line in afinn_file:
        term, score = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    return scores


# Given an array of Strings processes all the words replaces the word with the processed word
def process_words(words, scores):
    proc_words = []
    for word in words:
        word = word.strip() # Remove trailing and preceeding white spaces.
        # filter word or phrases removing punctuations, Quotations symbols.
        # add the sentiment score of the word to the ongoing SUM
        word = "".join(c for c in word if c not in ('!', '.', ':', ',', '?', '"'))  # Remove extra characters
        if len(word) == 0 or word.find('@') != -1:
            continue
        proc_words.append(word.lower())
    # Find all the words not in the AFINN file
    for word in proc_words:
        if word not in scores:
            # Add the current word
            add_word_for_relations(word)
            # Iterate through the other words add the association
            for other_word in proc_words:
                if other_word == word:
                    continue
                add_association(word, other_word, scores)

    return proc_words

# Adds a potential bidirectional association if one of the words is in AFINN-111.txt
def add_association(word1, word2, scores):
    # If both words have predefined scores then ignore it
    # If both words do not have predefined scores then ignore it because there is not relation.
    if word1 in scores and word2 in scores or word1 not in scores and word2 not in scores:
        return

    # Correctly assign the word to be tracked and the word with new score
    if word1 in scores:
        word_with_score = word1
        word_without_score = word2
    else:
        word_with_score = word2
        word_without_score = word1
    add_word_for_relations(word_without_score)

    # Update the correct mapping
    if word_without_score in associated_words:
        associated_words[word_without_score].append(word_with_score)


# Adds the word to the negative and positive world association
def add_word_for_relations(word):
    if word not in associated_words and not word.startswith("@"):
        associated_words[word] = []

# Calculate the Sentiment of a given term.
def calculate_sentiment(words, known_scores):
    # For every word in the tweet's text
    for word in words:
        # If the word already has an associated sentiment score, continue to next word.
        if word in known_scores:
            continue
        # If the word does not have a score check if the word is associated
        # to a word that had an original sentiment score.
        elif word in associated_words:
            # Calculate the negative and positive weight
            sent_words = associated_words[word]
            pos_sent_score = 0
            neg_sent_score = 0
            # Appropriately assign the value to the negative or positive some
            for sent_word in sent_words:
                score = known_scores[sent_word]
                if score < 0:
                    neg_sent_score += score
                else:
                    pos_sent_score += score
            # If the score is the same assign the score of "word" to 0
            if pos_sent_score == neg_sent_score:
                known_scores[word] = 0
            elif pos_sent_score == 0:
                known_scores[word] = neg_sent_score
            elif neg_sent_score == 0:
                known_scores[word] = pos_sent_score
            else:
                # calculate the weights based off of x = pos_sent_score / abs(neg_sent_score)
                # if x is less then one, x = - 1 / x
                x = float(pos_sent_score) / float(abs(neg_sent_score))
                if x < 1:
                    x = - (1.0 / x)
                known_scores[word] = x

def main():
    if not (len(sys.argv) == 2 or len(sys.argv) == 3):
        raise ValueError('Incorrect argument signature\n Correct signature: '
                         'frequency.py <tweet_file> <output_file>(Optional)')
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        raise ValueError('Argument is not a file')
    if len(sys.argv) == 3 and os.path.isfile(sys.argv[2]):
        raise ValueError('Output Argument is not a file')
    tweet_file = open(file_path)  # The first file will should have all the tweets per line

    # Populate the Sentiment Library
    scores = build_scores_dictionary()

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
        words = process_words(words, scores)
        calculate_sentiment(words, scores)

    # Close the files for the tweets
    tweet_file.close()

    # Ensure the output values for all the word are in fact floats and ints
    for key in scores:
        val = scores[key]
        if not (type(val) is int or type(val) is float):
            raise ValueError("Word \"" + key + "\" has incorrect value \"" + str(val) + "\" " + str(type(val)))

    lines = []
    for key in scores:
        lines.append(key + " " + str(scores[key]) + "\n")
    output = ''.join(lines)

    if len(sys.argv) == 2:
        print(output)
    else:
        output_file = open(sys.argv[2], 'w')
        output_file.write(output)
        output_file.close()

if __name__ == '__main__':
    main()
