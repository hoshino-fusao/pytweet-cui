# -*- coding: utf-8 -*-
from sys import stdin, stdout, exit
import random
from cmd import Cmd
import urllib
import urllib2
import tweepy
from tweepy.error import TweepError

import settings
from lib import parseargs

class TwitterClient(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = settings.PROMPT
        self.key = settings.ACCESS_TOKEN
        self.secret = settings.ACCESS_TOKEN_SECRET
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(self.key, self.secret)
        self.api = tweepy.API(auth)
        self.auth = auth
        self.me = self.api.me()
        print "%s logged in" % self.me.screen_name

    def emptyline(self):
        pass

    def do_EOF(self, args):
        print
        print random.choice(settings.EXIT_MESSAGES)
        exit()

    def do_timeline(self, args):
        parsed_args = parseargs(args)
        if parsed_args is None:
            print "Unable parse arguments."
            return

        count = parsed_args.get('count') or parsed_args.get('c') or 30
        timeline = self.api.home_timeline(count=count)
        timeline.reverse()
        for status in timeline:
            print settings.STATUS_TEMPLATE.format(
                date = status.created_at,
                name = status.user.screen_name,
                status = status.text.encode(self.stdout.encoding),
            ) 

    def do_retweet (self, mode="by_me",count=30):
        retweet = ""
        if mode == "by_me":
            retweet = self.api.retweeted_by_me(count=count)
        elif mode == "to_me":
            retweet = self.api.retweeted_to_me(count=count)
        elif mode == "of_me":
            retweet = self.api.retweets_of_me(count=count)

        for status in retweet:
            print settings.STATUS_TEMPLATE.format(
                date=status.created_at,
                name=status.user.screen_name,
                status=status.text.encode(stdout.encoding),
            ) 

    def do_mentions(self, count=30):
        mentions = self.api.mentions(count=count)
        mentions.reverse()
        for status in mentions:
            print settings.STATUS_TEMPLATE.format(
                date=status.created_at,
                name=status.user.screen_name,
                status=status.text.encode(stdout.encoding)
            )

    def do_tweet(self, message):
        status = message.decode(stdin.encoding).encode(stdout.encoding)
        self.api.update_status(status)
        
        if settings.FACEBOOK_ACCESS_TOKEN:
            data = dict(access_token=settings.FACEBOOK_ACCESS_TOKEN, message=status)
            urllib2.urlopen("https://graph.facebook.com/me/feed", urllib.urlencode(data))

    def do_lists(self, args):
        lists = self.api.lists()
        if lists:
            for l in lists:
                print "{full_name} {description}".format(
                    full_name = l.full_name.encode(stdout.encoding),
                    description = l.description.encode(stdout.encoding)
                )
        else:
            print "You have no lists."

    def do_list(self, slug, count=30):
        if not slug:
            print "list [list name]"
            return

        try:
            timeline = self.api.list_timeline(owner=self.me.screen_name, slug=slug, count=count)
            timeline.reverse()
            for status in timeline:
                print settings.STATUS_TEMPLATE.format(
                    date=status.created_at,
                    name=status.user.screen_name,
                    status=status.text.encode(stdout.encoding)
                )
        except TweepError as e:
            if e.response.status == 404:
                print "List does not exist."
            else:
                print e.reason

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
            print settings.STATUS_TEMPLATE.format(
                date = result.created_at,
                name = result.from_user,
                status = result.text.encode(stdout.encoding)
            )

    def do_favorites(self, user_name):
        user_id = None

        if user_name:
            user_id = self.api.get_user(user_name).id

        favorites = self.api.favorites(user_id)
        favorites.reverse()

        for status in favorites:
            print settings.STATUS_TEMPLATE.format(
                date = status.created_at,
                name = status.user.screen_name,
                status = status.text.encode(stdout.encoding)
            )

    def do_fav(self, id):
        self.api.create_favorite(id)

    def do_unfav(self, id):
        self.api.destroy_favorite(id)


if __name__ == "__main__":
    client = TwitterClient()
    try:
        client.cmdloop()
    except KeyboardInterrupt:
        client.onecmd("EOF")

