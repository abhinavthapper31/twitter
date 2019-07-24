import tweepy
from bs4 import BeautifulSoup
import re

#keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

def get_user_tweets(query):
	#authenticate
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	final = []


	new_tweets = api.user_timeline(id=query, count=200)
	for tweet in new_tweets:
		if (not tweet.retweeted) and ('RT @' not in tweet.text) :
			final.append(tweet)

	oldest_id = final[-1].id

	final_size = len(final)
	print(final_size)
	prev = 0
	while len(final) <= 3000:
		print("Getting tweets before %s" % (oldest_id))

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(id=query,count=200,max_id=oldest_id)
		
		#add new tweets
		for tweet in new_tweets:
			if (not tweet.retweeted) and ('RT @' not in tweet.text) :
				final.append(tweet)
		if(prev == len(final)):
			break ;

		#update the id of the oldest tweet less one
		oldest_id = final[-1].id - 1

		print ("...%s tweets downloaded so far" % (len(final)))
		prev = len(final)
	return final


def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(r'@[\w_]+|https?://[A-Za-z0-9./]+|\#+[\w_]+[\w\'_\-]*[\w_]+', ' ', souped)
    stripped = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", stripped)
    stripped = re.sub('[^a-zA-Z]', ' ', stripped)
    stripped = re.findall(r'.+',stripped)
    clean = " ".join(stripped)
    return clean.strip()


query = raw_input('Enter the user handle of the person whose tweet you want to predict : ') ;

collection = get_user_tweets(query)

#cleaning
for tweet in collection:
	print(tweet_cleaner(tweet.text))