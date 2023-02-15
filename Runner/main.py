from module.scraper import TweetScraper

# create helper objects
tweetScraper = TweetScraper()

# set parameters
topic_title = 'ISRO'
query = '@isro'
limit = 10

# scrape tweets
rawData = tweetScraper.get_tweets(query, limit)
print(rawData)
