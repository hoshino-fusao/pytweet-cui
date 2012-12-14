# -*- coding: utf-8 -*-
from cmd import Cmd
from dateutil.relativedelta import relativedelta
from sys import stdin, stdout, exit
import random
import urllib
import urllib2
import textwrap

import tweepy
from tweepy.error import TweepError

import settings
from lib import parseargs
from decorators import print_exception_message

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
        self.tmp_ids = []
        print "%s logged in" % self.me.screen_name
        print

    def emptyline(self):
        pass

    def do_EOF(self, args):
        print
        print random.choice(settings.EXIT_MESSAGES)
        exit()

    @print_exception_message(TweepError)
    def do_timeline(self, args):
        parsed_args = parseargs(args, default_key='count')
        count = parsed_args.get('count') or 30

        timeline = self.api.home_timeline(count=count)
        timeline.reverse()
        self.tmp_ids = []
        for i, status in enumerate(timeline):
            self.status_template(i, status)
            self.tmp_ids.append(status.id)

    def do_retweet (self, mode="by_me",count=30):
        retweet = ""
        if mode == "by_me":
            retweet = self.api.retweeted_by_me(count=count)
        elif mode == "to_me":
            retweet = self.api.retweeted_to_me(count=count)
        elif mode == "of_me":
            retweet = self.api.retweets_of_me(count=count)

        self.tmp_ids = []
        for i, status in enumerate(retweet):
            self.status_template(i, status)
            self.tmp_ids.append(status.id)

    @print_exception_message(TweepError)
    def do_mentions(self, args):
        parsed_args = parseargs(args, default_key='count')
        count = parsed_args.get('count') or 30

        mentions = self.api.mentions(count=count)
        mentions.reverse()
        self.tmp_ids = []
        for i, status in enumerate(mentions):
            self.status_template(i, status)
            self.tmp_ids.append(status.id)

    @print_exception_message(TweepError)
    def do_tweet(self, args):
        parsed_args = parseargs(args, default_key='message')
        status = parsed_args.get('message').decode(stdin.encoding).encode(stdout.encoding)
        self.api.update_status(status)
        
        if settings.FACEBOOK_ACCESS_TOKEN:
            data = dict(access_token=settings.FACEBOOK_ACCESS_TOKEN, message=status)
            urllib2.urlopen("https://graph.facebook.com/me/feed", urllib.urlencode(data))

    @print_exception_message(TweepError)
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


    def help_list(self):
        print textwrap.dedent("""\
                usage:
                list <slug>|slug=<slug> [count=<limit the number of statuses output>]

                Try 'lists' to get more slug.
                """)

    @print_exception_message(TweepError)
    def do_list(self, args):
        parsed_args = parseargs(args, default_key='slug')
        count = parsed_args.get('count') or 30
        slug = parsed_args.get('slug') or None

        if slug is None:
            self.onecmd('help list')
            return

        timeline = self.api.list_timeline(owner=self.me.screen_name, slug=slug, count=count)
        timeline.reverse()
        self.tmp_ids = []
        for i, status in enumerate(timeline):
            self.status_template(i, status)
            self.tmp_ids.append(status.id)

    def help_search(self):
        print textwrap.dedent("""\
                usage:
                search <query string>
                """)

    @print_exception_message(TweepError)
    def do_search(self, args):
        parsed_args = parseargs(args, default_key='query')
        query = parsed_args.get('query') or None
        if query is None:
            self.onecmd('help search')
            return

        results = self.api.search(query)
        if not results:
            print "No tweet results for %s." % query
            return

        results.reverse()
        self.tmp_ids = []
        for i, result in enumerate(results):
            print settings.STATUS_TEMPLATE.format(
                index = i,
                date = result.created_at,
                name = result.from_user,
                status = result.text.encode(stdout.encoding)
            )

            self.tmp_ids.append(result.id)

    
    def help_favorites(self):
        print textwrap.dedent("""\
                usage:
                favorites [<user name>]
                """)

    @print_exception_message(TweepError)
    def do_favorites(self, args):
        parsed_args = parseargs(args, default_key='user')
        user = parsed_args.get('user')

        user_id = None
        if user:
            user_id = self.api.get_user(user).id

        favorites = self.api.favorites(user_id)
        favorites.reverse()

        self.tmp_ids = []
        for i, status in enumerate(favorites):
            self.status_template(i, status)
            self.tmp_ids.append(status.id)


    def help_fav(self):
        print textwrap.dedent("""\
                usage:
                fav <index number>

                Try 'timeline' or 'search <query string>' to get index number of status.
                """)

    @print_exception_message(TweepError, IndexError)
    def do_fav(self, args):
        parsed_args = parseargs(args, default_key='index')
        index = parsed_args.get('index')
        if not index:
            self.onecmd('help fav')
            return

        self.api.create_favorite(self.tmp_ids[int(index)])


    def help_unfav(self):
        print textwrap.dedent("""\
                usage:
                unfav <index number>

                Try 'favorites' to get index number of status.
                """)

    @print_exception_message(TweepError, IndexError)
    def do_unfav(self, args):
        parsed_args = parseargs(args, default_key='index')
        index = parsed_args.get('index')
        if not index:
            self.onecmd('help unfav')
            return

        self.api.destroy_favorite(self.tmp_ids[int(index)])


    def status_template(self, index, status):
        print settings.STATUS_TEMPLATE.format(
            index = index,
            date = status.created_at + relativedelta(hours=+9),
            name = status.user.screen_name,
            status = status.text.encode(stdout.encoding),
        )


if __name__ == "__main__":
    client = TwitterClient()
    try:
        client.cmdloop()

    except KeyboardInterrupt:
        client.onecmd("EOF")

