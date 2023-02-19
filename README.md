# twitter-sentiment-analysis
This is a demo poc for sentiment analysis of tweets. 
The repo is divided into:
- [Notebooks](https://github.com/mratanusarkar/twitter-sentiment-analysis/tree/main/Notebooks)
- [Scripts](https://github.com/mratanusarkar/twitter-sentiment-analysis/tree/main/Runner)

Where you can find: 
- various experiments with Twitter API
- ways to scrape and collect tweet data using various kinds of search parameters 
- perform analysis and visualizations using the collected data
- Sentiment analysis and Insights using NLP

In the **Notebooks**, and a script/module format of the same in **Runner** folder for background running jobs.


# Features
This repo is still a work-in-progress. <br>
Some of the features currently implemented are as follows:

- Tweet Scraper
- Twitter Word Cloud
- (more features coming soon...)

---

# Tweet Scraper
This is a scrapper function used to gather and collect tweets, powered by [snscrape](https://github.com/JustAnotherArchivist/snscrape). <br>
compared to tweet API v2, this enables us to get unlimited tweets without any restrictions and without the need to get API tokens and secrets.

## usage:
Here is a sample usage:
```python
from module.scraper import TweetScraper

# create helper objects
tweet_scraper = TweetScraper()

# set parameters
query = '@isro'
limit = 1000

# scrape tweets
rawData = tweet_scraper.get_tweets(query, limit)
```
This will return a pandas dataframe containing last 1000 tweets from @isro. <br>
see the function signature below to get more details on function parameters.

## parameters

| Parameter | Data Type        | Description                                               | More Details                                                                                                                                                               |
|-----------|------------------|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| query     | string           | twitter search query as per https://twitter.com/search?q= | it can be a user mention like: `@user` or hashtag like `#tag` or a word like `text` or a complex query joined by  `AND`, `OR`, or statement enclosed in `()`               |
| limit     | int              | number of tweets you want to scrape                       | depending on number of tweets, the script will take time to execute. example: 100 tweets will be collected in 1s, where as 10,000 might take 5min and 1,00,000 may take 1h |
| return    | pandas dataframe | a pandas dataframe with the tweets                        | as of now, the following data fields are collected: `id`, `date`, `username`, `content`, `view_count`, `like_count`, `reply_count`, `retweet_count`, `quote_Count`, `url`  |

---

# Twitter Word Cloud
This is a visualization tool powered by [word_cloud](https://github.com/amueller/word_cloud).
Combined with the scraper function above, this tool gives you the capability to visualize what's going on in twitter at a glance!
In short, it uses all the tweets and counts the most occurring words in the tweets. It discards the common english words, and non-english characters, does pre-processing and data cleaning,
and In the end, you get a word cloud that gives insight into your search query.

For example:
- you can input @user and see what's going on with the user's timeline at one go!
- you may input a trending #hashtag and take a look on what twitter has to say on the trend/issue/event at one go!
- it's left to the end user on how they may use this tool and get powerful visualization. the possibilities are limitless!

I am sharing a few use-cases below.

## sample use case:
TODO

## usage:
Here is a sample usage:
```python
from module.scraper import TweetScraper
from module.generator import TwitterWordCloud

# create helper objects
tweet_scraper = TweetScraper()
tweet_wc = TwitterWordCloud()

# set parameters
topic_title = 'ISRO During SSLV-D2 Launch'
query = 'ISRO (#SSLVD2 OR #ISRO)'
limit = 1000
exclude_words = ['amp', 'eval']

# scrape tweets
rawData = tweet_scraper.get_tweets(query, limit)
tweet_wc.generate_word_cloud_v2(rawData, topic_title, exclude_words, 1080, 720)
```

This will generate a wordcloud using last 1000 tweets made during the ISRO SSLV-D2 Launch.
see the function signature below to get more details on function parameters.

## parameters

### function: generate_word_cloud():
a simple generator function with with only one required parameter (the dataframe) for quick easy word cloud generation. <br>
The output image is (1000px, 500px) in a (15, 8) inch canvas.

| Parameter           | Data Type        | Description                                              | More Details                                                                                                            |
|---------------------|------------------|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| rawData             | pandas dataframe | pandas dataframe from scraper function                   |                                                                                                                         |
| force_exclude_words | list of strings  | words you wish to exclude from word cloud                | after seeing an output, if you feel some words from the image that you wish to exclude, you can do so using this option |
| return              | None             | it generates and display the wordcloud, and saves as png |                                                                                                                         |

### generate_word_cloud_v2():
a move customizable and generic function with the following parameters

| Parameter           | Required         | Data Type        | Description                                                    | More Details                                                                                                            |
|---------------------|------------------|------------------|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| rawData             | Yes              | pandas dataframe | pandas dataframe from scraper function                         |                                                                                                                         |
| topic_title         | Yes              | string           | a short string describing the topic of tweets in the dataframe | the output files will have the same name as the topic                                                                   |
| force_exclude_words | No, default []   | list of strings  | words you wish to exclude from word cloud                      | after seeing an output, if you feel some words from the image that you wish to exclude, you can do so using this option |
| width               | No, default 1000 | int              | number of pixels wide of the output image                      |                                                                                                                         |
| height              | No, default 500  | int              | number of pixels height of the output image                    |                                                                                                                         |
| dpi                 | No, default 100  | int              | pixel density per inch                                         |                                                                                                                         |
| return              | NA               | None             | it generates and display the wordcloud, and saves as png       |                                                                                                                         |

---