import json
import os
import sys

__author__ = 'Michael Hotan'


def count_hashtags(hashtags, count_map):
    for hashtag in hashtags:
        text = hashtag['text'].lower()
        if not text in count_map:
            count_map[text] = 1
        else:
            count_map[text] += 1


def calculate_total_hashtags(count_map):
    total = 0
    for key in count_map:
        total += count_map[key]
    return total

def calculate_frequency(key, count_map):
    return float(count_map[key]) / float(calculate_total_hashtags(count_map))


def main():
    # Check parameter signature
    if not len(sys.argv) == 2:
        raise ValueError('Incorrect argument signature\n Correct signature: '
                         'top_ten.py <tweet_file>')
    tweet_file_path = sys.argv[1]
    if not os.path.isfile(tweet_file_path):
        raise ValueError('Tweet file Argument is not a file')
    tweet_file = open(tweet_file_path)  # The first file will should have all the tweets per line

    # The Count map
    hashtag_count = {}

    for tweet_json_line in tweet_file.readlines():
        tweet = json.loads(tweet_json_line)
        if 'entities' in tweet:
            if 'hashtags' in tweet['entities']:
                count_hashtags(tweet['entities']['hashtags'], hashtag_count)

    # Clean up the file
    tweet_file.close()

    frequencies = {}
    for key in hashtag_count:
        frequencies[key] = calculate_frequency(key, hashtag_count)

    sorted_hashtags = sorted(frequencies.items(), key=lambda hashtag: hashtag[1], reverse=True)
    for idx in range(min(10, len(sorted_hashtags))):
        print "{0} {1}".format(sorted_hashtags[idx][0].encode('utf-8'), sorted_hashtags[idx][1])

if __name__ == '__main__':
    main()