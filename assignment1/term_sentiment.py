import sys

def build_scores_dictionary():
    afinn_file = open("AFINN-111.txt")
    scores = {} # initialize an empty dictionary
    for line in afinn_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    print scores.items()  # Print every (term, score) pair in the dictionary
    return scores

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    tweet_file = open(sys.argv[1])  # The first file will should have all the tweets per line
    hw()
    lines(sent_file)
    lines(tweet_file)

if __name__ == '__main__':
    main()
