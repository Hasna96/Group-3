import tweepy
from tweepy import OAuthHandler
import csv
# coding=UTF-8
import nltk
from nltk.corpus import brown
# -*- coding: utf-8 -*-
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize


# change the location for stanford tagger
st = StanfordNERTagger('/Users/Hasna/Desktop/stanford-ner-2016-10-31/classifiers/english.muc.7class.distsim.crf.ser.gz',
					   '/Users/Hasna/Desktop/stanford-ner-2016-10-31/stanford-ner.jar',
					   encoding='utf-8')


### AUTHENTICATE ############################################################

# Authenticating with Twitter App
consumer_key = 'V4DwZPB6fGwsgUN5h27Cmv1zi'
consumer_secret = 'DJh4h0FaEgCeGZ5GwCWE5Pxvp1vHtpWfNkIGtk896dzGgIf51K'
access_token = '741486000-T0sijZatp5ZmxbA0MgHwgtqGKjh4WNKHhP3IqquJ'
access_secret = 'D89rXSqveZLLnfVWnf8jS1SX2jn7TlYnZ7TAvT9JBTajh'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

### RETRIEVES TWEETS FROM CARDIFF AREA ###########################

tweet_id = 0
tweet = ''
tweet_ids = []
tweet_dict = {}

# Specifies tweets being queried by search criteria ("q") and geocode
cardiff_tweets = tweepy.Cursor(api.search, q = '', geocode = "51.49675,-3.19229,16km").items(30)

# Loop through returned tweets
for tweet in cardiff_tweets:
	tweet_id += 1
	tweet_ids.append (tweet_id)
	tweet_string = str(tweet.text)
	tweet_dict[tweet_id] = tweet_string

#print(tweet_dict)


# This is our fast Part of Speech tagger
#############################################################################
brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'(I|i)$', 'PRP'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is our semi-CFG; will Extend it according to our own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"
#############################################################################


class NPExtractor(object):

    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN" or t[1] == "JJ" or t[1] == "JJR" :
            #if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches


# Main method, just run "python nlp.py"
def main():
    
    for tweet in tweet_dict:

    
    	np_extractor = NPExtractor(tweet_dict[tweet])
    	result = np_extractor.extract()
    	print ("This tweet is about: %s" % ", ".join(result))
    
    	tokenized_text = word_tokenize((result[0]).title())
    	classified_text = st.tag(tokenized_text)

    	print(classified_text)
if __name__ == '__main__':
    main()
