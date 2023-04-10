import snscrape.modules.twitter as sntwitter
import pandas as pd
import traceback
from tqdm import tqdm


class TweetScraper:
    columns = [
        'id',
        'date',
        'username',
        'content',
        'view_count',
        'like_count',
        'reply_count',
        'retweet_count',
        'quote_Count',
        'url'
    ]

    def __init__(self, columns=[]):
        if columns:
            self.columns = columns

    def get_tweets(self, query: str, limit: int) -> pd.DataFrame:
        """
        Scrape tweets from twitter based on input search query
        Arguments:
            :param query: twitter search query as per https://twitter.com/search?q=
            :param limit: number of tweets you want to scrape
        Returns:
            :return: a pandas dataframe with the tweets
        """
        tweets = []
        columns = self.columns
        try:
            print("scraping tweets ...")
            twitter_search = sntwitter.TwitterSearchScraper(query).get_items()
            for tweet in tqdm(twitter_search, total=limit):
                if len(tweets) == limit:
                    break
                else:
                    data = [
                        tweet.id,
                        tweet.date,
                        tweet.user.username,
                        tweet.rawContent,
                        tweet.viewCount,
                        tweet.likeCount,
                        tweet.replyCount,
                        tweet.retweetCount,
                        tweet.quoteCount,
                        tweet.url
                    ]
                    tweets.append(data)
            df = pd.DataFrame(tweets, columns=columns)
            return df
        except Exception:
            print(traceback.print_exc())
            return pd.DataFrame()
