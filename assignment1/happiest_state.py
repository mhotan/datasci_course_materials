import codecs
import json
import os
import sys

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

__author__ = 'mhotan'

# The coordinate is [lat, long]

states = {
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


# def print_names():
#     for state in states:
#         print state['name']
#
# def print_codes():
#     for state in states:
#         print state['code']

def print_states():
    for state in states:
        print states[state]

def find_state_by_name(name):
    # If the state name is actually equal to the name
    for code in states:
        if states[code].lower() == name:
            return code
    for code in states:
        if states[code].lower() in name:
            return code
    return None

def find_state_by_code(code):
    if code.upper() in states:
        return code
    return None

def find_code_by_name(name):
    for code in states:
        if states[code].strip().lower() == name.strip().lower():
            return code
    return None

# def find_borders_by_code(code):
#     state = find_state_by_code(code)
#     if not state is None:
#         return get_border_from_state(state)

# def find_borders_by_name(name):
#     state = find_state_by_name(name)
#     if not state is None:
#         return get_border_from_state(state)

# def get_border_from_state(state):
#     return state['borders'][0]

# def point_in_borders(lat, long, borders):
#     return False
#
#     n = len(borders)
#     inside = False
#
#     p1_lat = borders[0][0]
#     p1_long = borders[0][1]
#     for i in range(n+1):
#         p2_lat = borders[i % n][0]
#         p2_long = borders[i % n][1]
#         if long > min(p1_long, p2_long):
#             if long <= max(p1_long, p2_long):
#                 if lat <= max(p1_lat, p2_lat):
#                     if p1_long != p2_long:
#                         xints = (long - p1_long) * (p2_lat - p1_lat) / (p2_long - p1_long) + p1_lat
#                     if p1_lat == p2_lat or lat <= xints:
#                         inside = not inside
#         p1_lat = p2_lat
#         p1_long = p2_long
#     return inside

# def get_containing_state(lat, long):
#     for state in states:
#         if point_in_borders(lat, long, get_border_from_state(state)):
#             return state
#     return None

def extract_states_from_full_name(full_name):
    # Split the String
    words = full_name.split(" ")
    proc_words = []
    for word in words:
        word = word.strip() # Remove trailing and preceeding white spaces.
        # Remove extra characters
        word = "".join(c for c in word if c not in ('!', '.', ':', ',', '?', '"', '(', ')', ';')).strip()
        proc_words.append(word)

    # Look for country code in any of the words.
    for word in proc_words:
        code = find_state_by_code(word)
        if not code is None:
            return [code.upper()]

    # Find any word that equals the state.
    for word in proc_words:
        code = find_state_by_name(word)
        if not code is None:
            return [code.upper()]

    return None

# def extract_states_from_coordinates(coordinates):
#     states_found = []
#     for coordinate in coordinates:
#         state = get_containing_state(coordinate[1], coordinate[0])
#         if not state is None:
#             states_found.append(state)
#     return set(states_found)


# Returns an array of states found.
def extract_states_from_place(tweet_json):
    found = False
    states_found = None
    if 'place' in tweet_json and not tweet_json['place'] is None:
        coordinates = tweet_json['place']['bounding_box']['coordinates']
        if coordinates is None or len(coordinates) == 0:
            # Extract name from other place.
            states_found = extract_states_from_full_name(tweet_json['place']['full_name'])
            found |= len(states_found) > 0
        # else:
        #     states_found = extract_states_from_coordinates(coordinates)
        #     found |= len(states_found) > 0
    if 'user' in tweet_json and not tweet_json['user'] is None and len(tweet_json['user']['location']) > 0 and not found:
        states_found = extract_states_from_full_name(tweet_json['user']['location'])

    if states_found is None or len(states_found) == 0:
        return None
    else:
        return states_found


def resolve_state(tweet_json, sentiment_score, score_mapping):
    states_found = extract_states_from_place(tweet_json)
    if states_found is None:
        return
    for code in states_found:
        score_mapping[code] += sentiment_score

def get_num(value):
    try:
        return int(value)
    except ValueError:
        return 0


# Main method that validates script parameters.
def main():
    if len(sys.argv) != 3:
        raise ValueError('Incorrect argument signature\n Correct signature: '
                         'happiest_state.py <sentiment_file> <tweet_file>')
    sentiment_path = sys.argv[1]
    if not os.path.isfile(sentiment_path):
        raise ValueError('Sentiment file name is not a file')
    tweet_path = sys.argv[2]
    if not os.path.isfile(tweet_path):
        raise ValueError('Sentiment file name is not a file')

    # Open the files
    sentiment_file = open(sentiment_path)
    tweet_file = open(tweet_path)

    sentiment_lines = sentiment_file.readlines()
    tweet_lines = tweet_file.readlines()

    # Mapping of state name to scores.
    state_score = {}
    for code in states:
        state_score[code] = 0

    sentiments = []
    # Read in all the sentiments
    for sentiment_line in sentiment_lines:
        sentiments.append(get_num(sentiment_line.strip()))

    # Process each tweet
    for idx in range(len(tweet_lines)):
        tweet_json = json.loads(tweet_lines[idx])
        resolve_state(tweet_json, sentiments[idx], state_score)

    # Clean up the files
    sentiment_file.close()
    tweet_file.close()

    sorted_scores = sorted(state_score.items(), key=lambda x: x[1], reverse=True)
    print str(sorted_scores[0][0]).upper()

if __name__ == '__main__':
    main()