#!/bin/bash
# Must generate bin/output.txt first by running "python twitterstream.py > bin/output.txt" for approx 3 minutes

# Make the output directory if it didn't exists for the first time.
mkdir -p bin

# Problem 1.2
rm -f bin/tweet_sentiment_output.txt
python tweet_sentiment.py AFINN-111.txt bin/output.txt > bin/tweet_sentiment_output.txt 
# Problem 1.3
rm -f bin/term_sentiment_output.txt
python term_sentiment.py bin/tweet_sentiment_output.txt bin/output.txt > bin/term_sentiment_output.txt
# Problem 1.4
rm -f bin/frequency_output.txt
python frequency.py bin/output.txt > bin/frequency_output.txt
# Problem 1.5
rm -f bin/happiest_state_output.txt
python happiest_state.py bin/tweet_sentiment_output.txt bin/output.txt > bin/happiest_state_output.txt
# Problem 1.6
rm -f bin/top_ten_output.txt
python top_ten.py bin/output.txt > bin/top_ten_output.txt