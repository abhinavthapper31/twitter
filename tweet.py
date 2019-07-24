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

nltk.download('stopwords')
sn = SenticNet('en')

for tweet in collection:
    tweet = tweet.lower()
    tweet = tweet.split()
    tweet = [word for word in tweet if not word in set(stopwords.words('english'))]
    tweet = ' '.join(tweet)
    print(tweet)

texts = [[word for word in document.lower().split()] for document in collection] #split list of tweets into indivisual words
dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

topWords = {}
for doc in corpus_tfidf:
    for iWord, tf_idf in doc:
        if iWord not in topWords:
            topWords[iWord] = 0

        if tf_idf > topWords[iWord]:
            topWords[iWord] = tf_idf


for i in enumerate(sorted(topWords.items(), key=lambda x: x[1], reverse=True), 1):
    print(dictionary.items())
    if i > 30:
        break

correlated_words = []
sentiment_vector = []
for i, item in enumerate(sorted(topWords.items(), key=lambda x: x[1], reverse=True), 1):
    try:
        correlated_words.append(dictionary[item[0]])
        sentiment_vector.append(sn.polarity_intense(dictionary[item[0]]))

        print(dictionary[item[0]], sn.polarity_intense(dictionary[item[0]]))

    except:
        continue
    if i == 30:
        break

print(correlated_words)
print(sentiment_vector)
