import sys
import json


def populate_association(word_lists, associations):
    """
    TODO
    :param word_lists:
    :param associations:
    :return:
    """
    # Kind of Ugly and potential memory hog.
    for word_list in word_lists:
        for word in word_list:
            if word not in associations:
                associations[word] = list()
            # Copying the word list the word was found in
            # NOTE: Ignoring all instances of the target "word" that exist in the list
            # This could result in strange behaviour for unscored words.
            word_list_copy = filter((lambda w: w != word), list(word_list))
            associations[word] = associations[word] + word_list_copy


def calculate_sentiment(scores):
    """
    Calculate the sentiment given a collection of scores
    :param scores: A list of scores
    :return: A single score
    """
    pos = 0
    neg = 0
    for score in scores:
        if score > 0:
            pos += score
        elif score < 0:
            neg += score

    # If the score is the same assign the score of "word" to 0
    if pos == neg:
        return 0
    elif pos == 0:
        return neg
    elif neg == 0:
        return pos
    else:
        x = float(pos) / float(abs(neg))
        if x >= 1:
            return x
        return -1.0 / x  # invert the fraction


def generate_score_dict(sent_file):
    scores = dict()
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores


def clean_word(word):
    """Given a word decode utf-8, remove all special characters, and lower case"""
    word = word.strip().encode('utf-8').lower()

    # NOTE: Might not have to do this if I am checking if a word contains sentiment
    exclude_chars = ['#', '!', '.', ':', ',', '?', '"', '(', ')', ';', '|', '-', ':', '#', '@', '&']
    for exclude_char in exclude_chars:
        word = word.replace(exclude_char, '')
    return word


def extract_words(tweet):
    """Given a JSON Twitter message extract and return a list of clean normalized words"""
    # For Tweets without the text field return an empty list of words
    if 'text' not in tweet:
        return []

    words = map(clean_word, tweet['text'].split(" "))
    words = filter((lambda w: w.isalnum()), words)
    return words


def extract_tweets(tweet_file):
    """Given a file containin a list of JSON tweet string return a collection of JSON objects"""
    return map((lambda line: json.loads(line.strip())), tweet_file.readlines())


def word_score(word, score_dict):
    """
    TODO
    :param word:
    :param score_dict:
    :return:
    """
    if word in score_dict:
        return score_dict[word]
    return 0


def main():
    """

    :return:
    """
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    score_dict = generate_score_dict(sent_file)
    associations = dict()
    word_lists = map(extract_words, extract_tweets(tweet_file))
    populate_association(word_lists, associations)
    new_terms = dict((term, v) for term, v in associations.iteritems() if term not in score_dict)
    for term in new_terms:
        new_terms[term] = map(lambda term: word_score(term, score_dict), new_terms[term])
        print '{0} {1}'.format(term, str(calculate_sentiment(new_terms[term])))




if __name__ == '__main__':
    main()
