import sys
import json


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


def term_list_to_count(term_list):
    counts = dict()
    for term in term_list:
        if term in counts:
            counts[term] += 1
        else:
            counts[term] = 1
    return counts


def extract_hashtags(tweets):
    # tags = map((lambda tag: tag.strip().encode('utf-8').lower()), tweet['entities']['hashtags'])
    has_hashtags_list = filter((lambda tweet: 'entities' in tweet and 'hashtags' in tweet['entities']), tweets)
    has_hashtags_list = filter((lambda l: l), has_hashtags_list)
    hashtags = map((lambda tweet: tweet['entities']['hashtags']), has_hashtags_list)
    hashtags = map((lambda tag_objects: map((lambda tag_object: tag_object['text'].encode('utf-8').lower()), tag_objects)), hashtags)
    hashtags = reduce((lambda l1, l2: l1 + l2), hashtags, [])
    # Currently Filtering out alphanumeric for clarity purposes.
    hashtags = filter((lambda w: w.isalnum()), hashtags)
    # Cant think of Python functional way of doing this.
    return hashtags


def extract_tweets(tweet_file):
    """Given a file containin a list of JSON tweet string return a collection of JSON objects"""
    return map((lambda line: json.loads(line.strip())), tweet_file.readlines())


def main():
    """

    :return:
    """
    tweet_file = open(sys.argv[1])
    hashtags = extract_hashtags(extract_tweets(tweet_file))
    counts = term_list_to_count(hashtags)
    freqs = calculate_frequencies(counts)
    for tag in sorted(freqs, key=(lambda s: freqs[s]), reverse=True)[:10]:
        print '{0} {1}'.format(tag, str(counts[tag]))


if __name__ == '__main__':
    main()
