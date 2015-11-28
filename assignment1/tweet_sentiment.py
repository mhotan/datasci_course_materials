import sys
import json
import functools


def clean_word(word):
    """Given a word decode utf-8, remove all special characters, and lower case"""
    word = word.strip().encode('utf-8').lower()

    # NOTE: Might not have to do this if I am checking if a word contains sentiment
    exclude_chars = ['#', '!', '.', ':', ',', '?', '"', '(', ')', ';', '\'', '|', '-', ':', '#', '@', '&']
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


def word_score(word1, word2, score_dict):
    """Given a word provide the adequate score of that word using the score dictionary"""
    if word1 in score_dict and word2 in score_dict:
        return score_dict[word1] + score_dict[word2]
    if word1 in score_dict:
        return score_dict[word1]
    if word2 in score_dict:
        return score_dict[word2]
    return 0


def generate_score_dict(sent_file):
    scores = dict()
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    s = generate_score_dict(sent_file)

    tweet_jsons = map((lambda line: json.loads(line.strip())), tweet_file.readlines())
    word_lists = map(extract_words, tweet_jsons) # Array of valuable words per tweet
    scores = map((lambda word_list: reduce(functools.partial(word_score, score_dict=s), word_list, 0)), word_lists)
    for score in scores:
        print score

if __name__ == '__main__':
    main()
