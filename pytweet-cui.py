# -*- coding: utf-8 -*-
from sys import stdin, stdout, exit
import random
from cmd import Cmd
import urllib
import urllib2
import tweepy

from settings import *

class TwitterClient(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = PROMPT
        self.key = ACCESS_TOKEN
        self.secret = ACCESS_TOKEN_SECRET
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(self.key, self.secret)
        self.api = tweepy.API(auth)
        self.auth = auth
        print "%s logged in" % self.api.me().screen_name

    def do_EOF(self, parameters):
        print
        print random.choice(EXIT_MESSAGES)
        exit()

    def emptyline(self):
        pass

    def do_timeline(self, count=30):
        timeline = self.api.home_timeline(count=count)
        timeline.reverse()
        for status in timeline:
            print STATUS_TEMPLATE.format(
                date=status.created_at,
                name=status.user.screen_name,
                status=status.text.encode(stdout.encoding)
            )

    def do_mentions(self, count=30):
        mentions = self.api.mentions(count=count)
        mentions.reverse()
        for status in mentions:
            print STATUS_TEMPLATE.format(
                date=status.created_at,
                name=status.user.screen_name,
                status=status.text.encode(stdout.encoding)
            )

    def do_tweet(self, message):
        status = message.decode(stdin.encoding).encode(stdout.encoding)
        self.api.update_status(status)
        
        if FACEBOOK_ACCESS_TOKEN:
            data = dict(access_token=FACEBOOK_ACCESS_TOKEN, message=status)
            urllib2.urlopen("https://graph.facebook.com/me/feed", urllib.urlencode(data))

    def do_search(self, query):
        if not query:
            print "search [query string]"
            return

        results = self.api.search(query)
        if not results:
            print "No tweet results for %s." % query
            return

        results.reverse()
        for result in results:
            print STATUS_TEMPLATE.format(
                date = result.created_at,
                name = result.from_user,
                status = result.text.encode(stdout.encoding)
            )


if __name__ == "__main__":
    client = TwitterClient()
    try:
        client.cmdloop()
    except KeyboardInterrupt:
        client.onecmd("EOF")

