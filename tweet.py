#import libraries
import re
import tweepy
#import unicodedata2
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from unidecode import unidecode
from gensim import corpora, models
from senticnet.senticnet import SenticNet

def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(r'@[\w_]+|https?://[A-Za-z0-9./]+|\#+[\w_]+[\w\'_\-]*[\w_]+', ' ', souped)
    stripped = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", stripped)
    stripped = re.sub('[^a-zA-Z]', ' ', stripped)
    stripped = re.findall(r'.+',stripped)
    clean = " ".join(stripped)
    return clean.strip()

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

maxTweets = 10000
tweetsPerQry = 1000

tweetCount = 0
searchQuery=raw_input('Enter keywords to search for:')
restype='popular'
language='en'
collection=[]

for tweet in tweepy.Cursor(api.search,q=searchQuery,result_type=restype,lang=language,tweet_mode='extended').items(maxTweets) :
   	if (not tweet.retweeted) and ('RT @' not in tweet.full_text) :
   		collection.append(tweet_cleaner(tweet.full_text))
   		tweetCount += 1

print("Downloaded {0} tweets".format(tweetCount))

for tweet in collection:
    tweet = tweet.lower()
    tweet = tweet.split()
    tweet = [word for word in tweet if not word in set(stopwords.words('english'))]
    tweet = ' '.join(tweet)
    print(tweet)

