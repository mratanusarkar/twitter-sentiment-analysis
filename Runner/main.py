from module.scraper import TweetScraper
from module.generator import TwitterWordCloud

# create helper objects
tweet_scraper = TweetScraper()
tweet_wc = TwitterWordCloud()

# set parameters
topic_title = 'ISRO'
query = '@isro'
limit = 10
exclude_words = []

# scrape tweets
rawData = tweet_scraper.get_tweets(query, limit)
tweet_wc.generate_word_cloud_v2(rawData, topic_title, exclude_words, 1080, 720)
