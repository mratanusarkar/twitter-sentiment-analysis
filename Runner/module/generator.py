import pandas as pd
import os
import string
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter


class TwitterWordCloud:

    def __init__(self):
        pass

    def refine_text(self, tweet: str) -> str:
        tweet_words = []
        for word in tweet.split(' '):
            if word.startswith('@') and len(word) > 1:
                # remove mentions
                word = ""
            elif word.startswith('http') or word.startswith('www'):
                # remove links
                word = ""
            tweet_words.append(word)
        refined_tweet = " ".join(tweet_words)

        # remove punctuations
        exclude = set(string.punctuation)
        refined_tweet = ''.join(ch for ch in refined_tweet if ch not in exclude)

        # remove non-printable characters (remove non english characters)
        printable = set(string.printable)
        refined_tweet = ''.join(filter(lambda x: x in printable, refined_tweet))

        return refined_tweet

    def word_counter(self, tweet: str, counter: Counter) -> Counter:
        word_list = tweet.split(' ')
        word_count = Counter(word_list)
        return counter + word_count

    def remove_common_words(self, counter: Counter, force_exclude_words=[]) -> Counter:
        # https://www.textfixer.com/tutorials/common-english-words.php
        common_words = [
            "", "tis", "twas", "a", "able", "about", "across", "after", "aint",
            "all", "almost", "also", "am", "among", "an", "and", "any", "are", "arent",
            "as", "at", "be", "because", "been", "but", "by", "can", "cant", "cannot",
            "could", "couldve", "couldnt", "dear", "did", "didnt", "do", "does",
            "doesnt", "dont", "either", "else", "ever", "every", "for", "from", "get",
            "got", "had", "has", "hasnt", "have", "he", "hed", "hell", "hes", "her",
            "hers", "him", "his", "how", "howd", "howll", "hows", "however", "i",
            "id", "ill", "im", "ive", "if", "in", "into", "is", "isnt", "it", "its",
            "its", "just", "least", "let", "like", "likely", "may", "me", "might", "mightve",
            "mightnt", "most", "must", "mustve", "mustnt", "my", "neither", "no", "nor",
            "not", "of", "off", "often", "on", "only", "or", "other", "our", "own", "rather",
            "said", "say", "says", "shant", "she", "shed", "shell", "shes", "should",
            "shouldve", "shouldnt", "since", "so", "some", "than", "that", "thatll",
            "thats", "the", "their", "them", "then", "there", "theres", "these", "they",
            "theyd", "theyll", "theyre", "theyve", "this", "tis", "to", "too", "twas",
            "us", "wants", "was", "wasnt", "we", "wed", "well", "were", "were", "werent",
            "what", "whatd", "whats", "when", "when", "whend", "whenll", "whens", "where",
            "whered", "wherell", "wheres", "which", "while", "who", "whod", "wholl",
            "whos", "whom", "why", "whyd", "whyll", "whys", "will", "with", "wont",
            "would", "wouldve", "wouldnt", "yet", "you", "youd", "youll", "youre", "youve", "your"]
        letters = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        ]
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        for word in common_words:
            try:
                counter.pop(word.lower())
                counter.pop(word.upper())
                counter.pop(word.title())
            except Exception:
                pass
        for word in letters + numbers:
            try:
                counter.pop(word.lower())
                counter.pop(word.upper())
            except Exception:
                pass
        if len(force_exclude_words) > 0:
            for word in force_exclude_words:
                try:
                    counter.pop(word)
                    counter.pop(word.lower())
                    counter.pop(word.upper())
                    counter.pop(word.title())
                except Exception:
                    pass
        return counter

    def generate_word_cloud(self, rawData: pd.DataFrame, force_exclude_words=[]):
        print("processing data & counting words ...")
        counter = Counter({})
        for tweet_content in tqdm(rawData.content, total=len(rawData.index)):
            refined_tweet = self.refine_text(tweet_content)
            counter = self.word_counter(refined_tweet, counter)
        counter = self.remove_common_words(counter, force_exclude_words)
        print("top 10 words:", counter.most_common(10))

        print("generating word cloud ...")
        wordcloud = WordCloud(width=1000, height=500).generate_from_frequencies(counter)
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.annotate(
            "@mratanusarkar", xy=(0.98, 0.02), xycoords='axes fraction',
            ha='right', va='bottom', fontsize=12, color='white', alpha=0.8, weight='bold'
        )
        fig = plt.gcf()
        # plt.show()
        return fig

    def generate_word_cloud_v2(self, rawData: pd.DataFrame, topic_title: str, force_exclude_words=[], width=1000, height=500,
                               dpi=100) -> None:
        """
        Generate word cloud from a pandas dataframe containing twitter data in a column named 'content'
        Arguments:
            :param rawData: pandas databrame with a column named 'content' that contents all the scraped tweets in string
            :param topic_title: name of the topic in string (name of the exported files)
            :param force_exclude_words: list of words (strings) that you want to be excluded from the wordcloud
            :param width: width of the canvas in px (default: 1000)
            :param height: height of the canvas in px (default: 500)
            :param dpi: dpi of the saved image (default: 100, same as matplotlib default)
        Returns:
            prints out the progress and shows the wordcloud
            :return: None
        """
        # process dataframe
        print("processing data & counting words ...")
        counter = Counter({})
        for tweet_content in tqdm(rawData.content, total=len(rawData.index)):
            refined_tweet = self.refine_text(tweet_content)
            counter = self.word_counter(refined_tweet, counter)
        counter = self.remove_common_words(counter, force_exclude_words)
        print("top 10 words:", counter.most_common(10))

        # generate word cloud
        print("generating word cloud ...")
        wordcloud = WordCloud(width=width, height=height).generate_from_frequencies(counter)

        # generate canvas and image from word cloud
        # inch to px conversion
        px = 1 / plt.rcParams['figure.dpi']
        plt.figure(figsize=(width * px, height * px))
        plt.imshow(wordcloud)
        plt.axis("off")
        # signature
        plt.annotate(
            "@mratanusarkar", xy=(0.98, 0.02), xycoords='axes fraction',
            ha='right', va='bottom', fontsize=12, color='white', alpha=0.8, weight='bold'
        )

        # Save Word Cloud
        img_file_path = "wordcloud/" + topic_title + str(width) + "x" + str(height) + ".png"
        os.makedirs(os.path.dirname(img_file_path), exist_ok=True)
        plt.savefig(img_file_path, bbox_inches='tight', dpi=dpi)
        print("completed", topic_title)
