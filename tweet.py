#import libraries
import re
import tweepy
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from unidecode import unidecode
from gensim import corpora, models
from senticnet.senticnet import SenticNet
from wordcloud import WordCloud
#import jsonify
from matplotlib import pyplot as plt


CONSUMER_KEY = 'TCvxTBBDsK1dY89hGYWa9Tza1'
CONSUMER_SECRET = 'HmWihgtLEIxcs9YaZgonHZzUclblxpzmb6Qk3urDJ2RsDrN5xn'
ACCESS_KEY = '981552284155850752-TG1E23llcrzDhCtc9CDIVg3dfTGlIWo'
ACCESS_SECRET = 'Y61RcyljzAJ3q145wfHrCwJk06CoGTedd8NVqJ4bAL6Ny'

def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(r'@[\w_]+|https?://[A-Za-z0-9./]+|\#+[\w_]+[\w\'_\-]*[\w_]+', ' ', souped)
    stripped = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", stripped)
    stripped = re.sub('[^a-zA-Z]', ' ', stripped)
    stripped = re.findall(r'.+',stripped)
    clean = " ".join(stripped)
    return clean.strip()

def tweetSearch(searchQuery,language,api):
    maxTweets = 100
    tweetsPerQry = 1
    tweetCount = 0
    collection = []
    for tweet in tweepy.Cursor(api.search,q=searchQuery,lang=language,tweet_mode='extended').items(maxTweets):
        if (not tweet.retweeted) and ('RT @' not in tweet.full_text) :
            collection.append(tweet_cleaner(tweet.full_text))
            tweetCount += 1

    print("Downloaded {0} tweets".format(tweetCount))




auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


searchQuery=raw_input('Enter keyword to search for:')
language='en'
collection=[]

collection = tweetSearch(searchQuery,language,api)

#nltk.download('stopwords')
#sn = SenticNet('en')

for tweet in collection:
    tweet = tweet.lower()
    tweet = tweet.split()
    tweet = [word for word in tweet if not word in set(stopwords.words('english'))]
    tweet = ' '.join(tweet)
    print(tweet+'\n')


wordcloud = WordCloud().generate(collection)
plt.figure(figsize=(12,6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

'''
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

'''