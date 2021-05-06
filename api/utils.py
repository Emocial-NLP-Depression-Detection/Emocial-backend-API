# Stop Words: A stop word is a commonly used word (such as “the”, “a”, “an”, “in”) that a search engine
# has been programmed to ignore, both when indexing entries for searching and when retrieving them
# as the result of a search query.
# -*- coding: utf-8 -*-


import string
import os
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from collections import Counter
import numpy as np
from tensorflow import keras
import tweepy
import tensorflow as td
import nltk
import re
import pandas as pd
from nltk.corpus import stopwords
from pythainlp.corpus import stopwords as stopwords_th
from pythainlp.tokenize import word_tokenize


def init():
    nltk.download('punkt')


nltk.download('stopwords')


# Stop Words: A stop word is a commonly used word (such as “the”, “a”, “an”, “in”) that a search engine
# has been programmed to ignore, both when indexing entries for searching and when retrieving them
# as the result of a search query.


def loaddata():

    # load dataset
    filename = './data/data-{}.csv'
    dataframe = pd.read_csv(filename)
    array = dataframe.values
    X = array[:, 0:2]
    Y = array[:, 2]
    return dataframe, X, Y


def cleanTxt(txt):
    txt = re.sub(r'@[A-Za-z0-9]+', '', str(txt))  # remove mentions
    txt = re.sub(r'#+', '', str(txt))  # remove '#'
    txt = re.sub(r'RT[\s]+', '', str(txt))  # remove RT
    txt = re.sub(r'https?:\/\/\S+', '', str(txt))  # remove links
    return txt


def remove_URL(text):
    url = re.compile(r"https?://\S+|www\.\S+")
    return url.sub(r"", text)

# https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate/34294022


def remove_punct(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


class DepressClassifier:
    def __init__(self, lang):
        # for testing
        self.lang = lang
        print(f"Importing {self.lang} data...")
        self.df = pd.read_csv(f"./data/data-{self.lang}.csv")
        self.df = self.df.sort_values(by=['label'])
        print("Finish Importing data.")
        # self.df = pd.read_csv(".\emocial\data\sentiment_tweets3.csv")

        print(f"Cleaning {self.lang} dataset...")
        self.df["Tweets"] = self.df.Tweets.map(
            remove_URL)  # map(lambda x: remove_URL(x))
        self.df["Tweets"] = self.df.Tweets.map(remove_punct)
        self.df["Tweets"] = self.df.Tweets.map(self.remove_stopwords)
        print(f"Done cleaning {self.lang} data.")
        
        self.counter = self.counter_word(self.df.Tweets)
        self.num_unique_words = len(self.counter)
        # Split dataset into training and validation set
        self.train_size = int(self.df.shape[0] * 0.8)
        self.tokenizer = Tokenizer(num_words=self.num_unique_words)
        self.train_df = self.df[:self.train_size]
        self.val_df = self.df[self.train_size:]

        # # split text and labels
        self.train_sentences = self.train_df.Tweets.to_numpy()
        self.train_labels = self.train_df.label.to_numpy()
        self.val_sentences = self.val_df.Tweets.to_numpy()
        self.val_labels = self.val_df.label.to_numpy()
        self.tokenizer.fit_on_texts(
            self.train_sentences)  # fit only to training
        self.word_index = self.tokenizer.word_index
        # self.train_sequences = self.tokenizer.texts_to_sequences(
        #     self.train_sentences)
        # self.val_sequences = self.tokenizer.texts_to_sequences(
        #     self.val_sentences)

        self.max_length = 20

        # self.train_padded = pad_sequences(
        #     self.train_sequences, maxlen=self.max_length, padding="post", truncating="post")
        # self.val_padded = pad_sequences(
        #     self.val_sequences, maxlen=self.max_length, padding="post", truncating="post")

    def counter_word(self, text_col):
        count = Counter()
        if self.lang == 'en':
            for text in text_col.values:
                for word in text.split():
                    count[word] += 1
            return count
        else:
            for text in text_col.values:
                for word in word_tokenize(text):
                    if word != ' ':
                        count[word] += 1
            return count

    def remove_stopwords(self, text):
        if self.lang == "en":
            stop = set(stopwords.words("english"))
            filtered_words = [word.lower()
                              for word in text.split() if word.lower() not in stop]
        if self.lang == "th":
            stop = stopwords_th.words("thai")
            filtered_words = [word.lower()
                              for word in word_tokenize(text) if word.lower() not in stop]

        return " ".join(filtered_words)

    def decode(self, sequence):
        return " ".join([self.reverse_word_index.get(idx, "?") for idx in sequence])

    def loadModel(self):
        self.model = keras.models.load_model(f"./models/model-{self.lang}.h5")
        self.loss = keras.losses.BinaryCrossentropy(from_logits=False)
        self.optim = keras.optimizers.Adam(lr=0.0083)
        self.metrics = ["accuracy"]

        self.model.compile(
            loss=self.loss, optimizer=self.optim, metrics=self.metrics)

    def review_encode(self, s):
        encoded = [1]

        for word in s:
            if word.lower() in self.word_index:
                encoded.append(self.word_index[word.lower()])
            else:
                encoded.append(2)

        return encoded

    def classify(self, list):
        
        self.loadModel()
        self.predictedData = pd.DataFrame([])
        for line in list:
            nline = line.replace(",", "").replace(".", "").replace("(", "").replace(
                ")", "").replace(":", "").replace("\"", "").strip().split(" ")
            self.encode = self.review_encode(nline)
            self.encode = keras.preprocessing.sequence.pad_sequences(
                [self.encode], padding="post", maxlen=20)  # make the data 250 words long
            self.predict = self.model.predict(self.encode)
            self.roundedPredict = round(float(self.predict[0]))
            print(line)
            print(self.encode)
            print(round(float(self.predict[0])))
            self.predictedData = self.predictedData.append(
                {'Tweet': line, 'Prediction': int(round(float(self.predict[0])))}, ignore_index=True)

    def classifyText(self, text):
        
        self.loadModel()
        nline = text.replace(",", "").replace(".", "").replace("(", "").replace(
            ")", "").replace(":", "").replace("\"", "").strip().split(" ")
        self.encode = self.review_encode(nline)
        self.encode = keras.preprocessing.sequence.pad_sequences(
            [self.encode], padding="post", maxlen=20)  # make the data 250 words long
        self.predict = self.model.predict(self.encode)
        self.roundedPredict = round(float(self.predict[0]))
        print(text)
        print(self.encode)
        print(round(float(self.predict[0])))


class TweetCaller:
    def __init__(self, lang):
        self.consumerkey = 'WLfzlzZ1ElU5ZlBtBpnttn1xt'
        self.consumersecret = '7RtI8JBF3aetK80Uqoil7dfMTyF5trXGQHyMKKHmSyzGXAnNO8'
        self.accesstoken = '1015944194966208512-rDnvf27WpOphOYl7yhwulKeLVncYAK'
        self.accesstokensecret = 'LOQ8x9p4hfABEQ44xfSV2vrPV7ooqMlGcI9Ld0fMjkLPO'
        self.auth = tweepy.OAuthHandler(self.consumerkey, self.consumersecret)
        self.auth.set_access_token(self.accesstoken, self.accesstokensecret)
        self.lang = lang
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    def callUser(self, username):
        self.twitterusername = username
        try:
            self.user = self.api.get_user(self.twitterusername)
            self.posts = self.api.user_timeline(
                screen_name=self.twitterusername, count=100, lang=self.lang, tweet_mode='extended')
            self.cannotFindUser = False
        except tweepy.TweepError:
            self.cannotFindUser = True

    def savePost(self):
        self.tweets = []
        for tweet in self.posts[0:]:
            if tweet.lang == self.lang:
                # print(tweet.full_text)
                self.tweets.append(str(tweet.full_text))

        # print(self.tweets)
        return self.tweets
