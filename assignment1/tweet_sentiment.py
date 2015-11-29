import sys
import json
import functools


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


def generate_score_dict(sent_file):
    scores = dict()
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores


def calculate_score(word_list, s):
    """
    Given a list of words and a score dictionary Calculate the score of the word
    :param word_list: a list of words to score and aggregate.
    :param score_dict: A dictionary of known words => sentiments
    :return: The score of the word list.
    """
    return reduce((lambda x1,x2: x1+x2), map((lambda x: word_score(x, score_dict=s)), word_list), 0)


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    s = generate_score_dict(sent_file)

    tweet_jsons = extract_tweets(tweet_file)
    word_lists = map(extract_words, tweet_jsons)  # Array of valuable words per tweet
    scores = map(functools.partial(calculate_score, s=s), word_lists)
    for score in scores:
        print score


if __name__ == '__main__':
    main()
