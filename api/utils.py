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


def init():
    nltk.download('punkt')


nltk.download('stopwords')


# Stop Words: A stop word is a commonly used word (such as “the”, “a”, “an”, “in”) that a search engine
# has been programmed to ignore, both when indexing entries for searching and when retrieving them
# as the result of a search query.


def loaddata():

    # load dataset
    filename = './data/sentiment_tweets3.csv'
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


def counter_word(text_col):
    count = Counter()
    for text in text_col.values:
        for word in text.split():
            count[word] += 1
    return count


def remove_URL(text):
    url = re.compile(r"https?://\S+|www\.\S+")
    return url.sub(r"", text)

# https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate/34294022


def remove_punct(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def remove_stopwords(text):
    stop = set(stopwords.words("english"))
    filtered_words = [word.lower()
                      for word in text.split() if word.lower() not in stop]
    return " ".join(filtered_words)


class DepressClassifier:
    def __init__(self, lang='en'):
        # for testing
        try:
            self.df = pd.read_csv(".\data\sentiment_tweets3.csv")
        except FileNotFoundError:
            self.df=None
        # self.df = pd.read_csv(".\emocial\data\sentiment_tweets3.csv")
        self.counter = counter_word(self.df.Tweets)
        self.num_unique_words = len(self.counter)
        self.lang = lang

    def initVar(self):
        self.cleanDF()
        self.counter = counter_word(self.df.Tweets)
        self.num_unique_words = len(self.counter)
        # Split dataset into training and validation set
        self.train_size = int(self.df.shape[0] * 0.8)
        self.tokenizer = Tokenizer(num_words=self.num_unique_words)
        self.train_df = self.df[:self.train_size]
        self.val_df = self.df[self.train_size:]

        # split text and labels
        self.train_sentences = self.train_df.Tweets.to_numpy()
        self.train_labels = self.train_df.label.to_numpy()
        self.val_sentences = self.val_df.Tweets.to_numpy()
        self.val_labels = self.val_df.label.to_numpy()
        self.tokenizer.fit_on_texts(
            self.train_sentences)  # fit only to training
        self.word_index = self.tokenizer.word_index
        self.train_sequences = self.tokenizer.texts_to_sequences(
            self.train_sentences)
        self.val_sequences = self.tokenizer.texts_to_sequences(
            self.val_sentences)

        self.max_length = 20

        self.train_padded = pad_sequences(
            self.train_sequences, maxlen=self.max_length, padding="post", truncating="post")
        self.val_padded = pad_sequences(
            self.val_sequences, maxlen=self.max_length, padding="post", truncating="post")

    def cleanDF(self):
        self.df["Tweets"] = self.df.Tweets.map(
            remove_URL)  # map(lambda x: remove_URL(x))
        self.df["Tweets"] = self.df.Tweets.map(remove_punct)
        self.df["Tweets"] = self.df.Tweets.map(remove_stopwords)

    def decode(self, sequence):
        return " ".join([self.reverse_word_index.get(idx, "?") for idx in sequence])

    def createModel(self):
        # Word embeddings give us a way to use an efficient, dense representation in which similar words have
        # a similar encoding. Importantly, you do not have to specify this encoding by hand. An embedding is a
        # dense vector of floating point values (the length of the vector is a parameter you specify).

        self.model = keras.models.Sequential()
        self.model.add(layers.Embedding(self.num_unique_words,
                                        32, input_length=self.max_length))

        # The layer will take as input an integer matrix of size (batch, input_length),
        # and the largest integer (i.e. word index) in the input should be no larger than num_words (vocabulary size).
        # Now model.output_shape is (None, input_length, 32), where `None` is the batch dimension.

        self.model.add(layers.LSTM(64, dropout=0.1))
        self.model.add(layers.Dense(1, activation="sigmoid"))

        print(self.model.summary())
        self.loss = keras.losses.BinaryCrossentropy(from_logits=False)
        self.optim = keras.optimizers.Adam(lr=0.001)
        self.metrics = ["accuracy"]

        self.model.compile(
            loss=self.loss, optimizer=self.optim, metrics=self.metrics)

    def trainModel(self):
        self.initVar()
        self.createModel()
        self.model.fit(self.train_padded, self.train_labels, epochs=5, validation_data=(
            self.val_padded, self.val_labels), verbose=2)

        self.model.save("./ai/model.h5", include_optimizer=False)

    def loadModel(self, dir):
        self.model = keras.models.load_model(dir)
        self.loss = keras.losses.BinaryCrossentropy(from_logits=False)
        self.optim = keras.optimizers.Adam(lr=0.001)
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
        self.initVar()
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
        self.initVar()
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
    def __init__(self):
        self.consumerkey = 'WLfzlzZ1ElU5ZlBtBpnttn1xt'
        self.consumersecret = '7RtI8JBF3aetK80Uqoil7dfMTyF5trXGQHyMKKHmSyzGXAnNO8'
        self.accesstoken = '1015944194966208512-rDnvf27WpOphOYl7yhwulKeLVncYAK'
        self.accesstokensecret = 'LOQ8x9p4hfABEQ44xfSV2vrPV7ooqMlGcI9Ld0fMjkLPO'
        self.auth = tweepy.OAuthHandler(self.consumerkey, self.consumersecret)
        self.auth.set_access_token(self.accesstoken, self.accesstokensecret)

        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    def callUser(self, username):
        self.twitterusername = username
        try:
            self.user = self.api.get_user(self.twitterusername)
            self.posts = self.api.user_timeline(
                screen_name=self.twitterusername, count=100, lang='en', tweet_mode='extended')
            self.cannotFindUser = False
        except tweepy.TweepError:
            self.cannotFindUser = True

    def savePost(self):
        self.tweets = []
        for tweet in self.posts[0:]:

            # print(tweet.full_text)
            self.tweets.append(str(tweet.full_text))

        # print(self.tweets)
        return self.tweets
