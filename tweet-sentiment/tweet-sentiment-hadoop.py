#!/usr/bin/env python
import sys
import json
import StringIO

_debug = 0
def msg_debug( message ):
    if _debug:
        print message

class emotion_scorer:
    scores = {}
    def __init__(self, inputdata):
        for line in inputdata:
            term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            self.scores[term] = int(score)  # Convert the score to an integer.
    def score(self,ngram):
        raw_words= ngram.lower().split()
        emotion_sum = 0
        num_emotions = 0
        for raw_word in raw_words:
            word = ''.join(e for e in raw_word if e.isalnum() )
            score = self.scores.get(word)
            if score is not None:
                msg_debug( word+" "+str(score))
                emotion_sum += score
                num_emotions += 1
        emotion_score = 0.0 if num_emotions == 0 else float(emotion_sum)/(num_emotions)
        msg_debug( ' '.join([str(emotion_score), str(emotion_sum), str(num_emotions)]) )
        return emotion_score

# Take a parsed JSON dict as a single tweet
class tweet:
    raw_data = {}
    unicode_tweet = u''
    ascii_text = ''
    emotion_score = 0.0
    def __init__(self, json_tweet):
        self.raw_data = json_tweet
        unicode_tweet = self.raw_data['text']
        self.ascii_text = unicode_tweet.encode('ascii','ignore')
    def score( self, scorer ):
        self.emotion_score = scorer.score( self.ascii_text )
        return self.emotion_score
    def display(self):
        msg_debug( self.ascii_text )
        print self.emotion_score

# Right now the reader is taking a constant file. Ideally it should take a stream
class twitter_reader:    
#    twitter_stream
    def __init__( self, stream ):
        self.twitter_stream = stream
    def load_tweet( self ):
        for line in self.twitter_stream:
            if line.find('{') == -1:
                continue
            response = json.loads(line)
            # There are strings in the stream that are not tweets
            if response.get('text') is not None:
                yield tweet( response )

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scorer = emotion_scorer(sent_file)
    reader = twitter_reader(tweet_file)
    for tweet in reader.load_tweet():
        tweet.score( scorer)
#        tweet.display()

if __name__ == '__main__':
    main()
