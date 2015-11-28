import sys

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))


def scores(sent_file):
    scores = dict()
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    s = scores(sent_file)
    print s

if __name__ == '__main__':
    main()
