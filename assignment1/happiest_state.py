import sys
import json
import functools


STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

for state in STATES:
    STATES[state] = STATES[state].upper()


def place(tweet):
    if "place" in tweet and tweet['place'] is not None:
        p = tweet["place"]
        content = [p["full_name"].encode('utf-8').upper(), p["name"].encode('utf-8').upper()]
        for c in content:
            for state in STATES:
                if state in c or STATES[state] in c:
                    return state
    return None


def generate_score_dict(sent_file):
    scores = dict()
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores


def extract_tweets(tweet_file):
    """Given a file containin a list of JSON tweet string return a collection of JSON objects"""
    return map((lambda line: json.loads(line.strip())), tweet_file.readlines())


def calculate_score(word_list, score_dict):
    """
    Given a list of words and a score dictionary Calculate the score of the word
    :param word_list: a list of words to score and aggregate.
    :param score_dict: A dictionary of known words => sentiments
    :return: The score of the word list.
    """
    return reduce(functools.partial(word_aggregate, score_dict=score_dict), word_list, 0)


def word_aggregate(word1, word2, score_dict):
    """Given a word provide the adequate score of that word using the score dictionary"""
    return word_score(word1, score_dict) + word_score(word2, score_dict)


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


def main():
    """

    :return:
    """
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = generate_score_dict(sent_file)

    tweets = extract_tweets(tweet_file)
    states = dict()
    for tweet in tweets:
        p = place(tweet)
        if p is None:
            continue
        if p in states:
            states[p].append(calculate_score(extract_words(tweet), scores))
        else:
            states[p] = [calculate_score(extract_words(tweet), scores)]
    for state in states:
        states[state] = float(reduce((lambda s1, s2: s1 + s2), states[state], 0)) / float(len(states[state]))
    ordered_states = sorted(states, key=(lambda s: states[s]), reverse=True)
    print ordered_states[0]


if __name__ == '__main__':
    main()