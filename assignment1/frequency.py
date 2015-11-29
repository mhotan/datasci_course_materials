import sys
import json


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


def term_list_to_count(term_list):
    counts = dict()
    for term in term_list:
        if term in counts:
            counts[term] += 1
        else:
            counts[term] = 1
    return counts


def merge_counts(counts1, counts2):
    """
    Given two mappings of words to counts combine the two dictionaries into one.

    When both counts have the same term the count is aggregated.

    :param counts1: Mapping of word to counts
    :param counts2: Different mapping of words to counts
    :return: Combined Count Mapping.
    """
    assert type(counts1) is dict, "Incorrect type {0}".format(str(type(counts1)))
    assert type(counts2) is dict, "Incorrect type {0}".format(str(type(counts2)))
    merged_counts = dict(counts1)
    for term in counts2:
        if term in merged_counts:
            merged_counts[term] += counts2[term]
        else:
            merged_counts[term] = counts2[term]
    return merged_counts


def word_count_for_tweets(tweet_objects):
    word_lists = map(extract_words, tweet_objects)  # Array of valuable words per tweet
    wordcounts = map(term_list_to_count, word_lists)  # Get per tweet word counts
    return reduce(merge_counts, wordcounts, dict())  # make mega word count dictionary


def total_word_count(counts):
    """
    Given a mapping of words to counts count the total amount of words
    :param counts: Mapping of word => count of that word
    :return: The total count of words for this mapping.
    """
    counts = map((lambda term: counts[term]), counts)
    return reduce((lambda c1, c2: c1 + c2), counts, 0)


def calculate_frequencies(counts):
    """
    Given a mapping of term to count calculate the frequency of each word
    :param counts: Mapping of term => count
    :return: The frequency of each word
    """
    freqs = dict()
    total = total_word_count(counts)
    for term in counts:
        freqs[term] = float(counts[term]) / float(total)
    return freqs


def extract_tweets(tweet_file):
    """Given a file containin a list of JSON tweet string return a collection of JSON objects"""
    return map((lambda line: json.loads(line.strip())), tweet_file.readlines())


def main():
    """
    Given
    :return:
    """
    tweet_file = open(sys.argv[1])

    tweet_jsons = extract_tweets(tweet_file)
    word_counts = word_count_for_tweets(tweet_jsons)
    freqs = calculate_frequencies(word_counts)
    for term in freqs:
        print '{0} {1}'.format(term, freqs[term])

if __name__ == '__main__':
    main()
