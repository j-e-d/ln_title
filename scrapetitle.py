#!/usr/bin/python3
import os
from lxml import html
import time
import sqlite3
import tweepy


def get_title(url, trailing):
    tree = html.parse(url)
    title = tree.find(".//title").text
    if title.endswith(trailing):
        thelen = len(trailing)
        title = title[:-thelen]
    return title


def get_last_title(c):
    c.execute("SELECT title FROM titles ORDER BY datetime DESC LIMIT 1")
    last_title = c.fetchone()
    if last_title is None:
        return last_title
    else:
        return last_title[0]


def insert_title(c, title):
    c.execute("INSERT INTO titles VALUES (?, ?)", (int(time.time()), title))


def tweet_title(title, api):
    api.update_status(title)
    return


def main():
    consumer_key = os.environ['LNTITLE_CONSUMER_KEY']
    consumer_secret = os.environ['LNTITLE_CONSUMER_SECRET']
    access_token = os.environ['LNTITLE_ACCESS_TOKEN']
    access_token_secret = os.environ['LNTITLE_ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    url = 'http://www.lanacion.com.ar/'
    trailing = ' - lanacion.com'
    title = get_title(url, trailing)
    print ("Curr. title: ", title)

    conn = sqlite3.connect('lntitles.db')
    c = conn.cursor()

    last = get_last_title(c)
    print ("Prev. title: ", last)
    if last != title:
        print ("New title, storing and tweeting")
        insert_title(c, title)
        tweet_title(title, api)
    else:
        print("Title didn't change, exiting")

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
