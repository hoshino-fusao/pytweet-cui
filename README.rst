コマンドラインのTwitterクライアント
===================================

.. image:: https://buildhive.cloudbees.com/job/ryuzi/job/pytweet-cui/badge/icon

twitter の設定
--------------

- https://dev.twitter.com/apps で以下の情報を取得します。
    * CONSUMER_KEY
    * CONSUMER_SECRET
    * ACCESS_TOKEN
    * ACCESS_TOKEN_SECRET
- settings-sample.py を settings.py としてコピーします。
- settings.py に、取得したtwitter情報を設定します。


Facebook の設定(オプション)
---------------------------

- https://developers.facebook.com/tools/explorer/ で ACCESS_TOKEN を取得します。
    * Extended Permissions で publish_stream にチェックをいててください。
- settings.py の FACEBOOK_ACCESS_TOKEN に上記で取得した内容を設定します。


参考URL
=======

- http://www.python.jp/doc/release/library/cmd.html
- https://dev.twitter.com/apps
- https://dev.twitter.com/docs/api/1.1
- https://github.com/tweepy/tweepy
- http://packages.python.org/tweepy/html/index.html

