# -*- coding: utf-8 -*-
from lib import parseargs
from nose.tools import eq_

class TestParseArgs:
    def test_normal(self):
        """ normal value """
        parsed = parseargs('count=2 message=test')
        eq_(parsed.get('count'), '2')
        eq_(parsed.get('message'), 'test')

    def test_empty(self):
        """ empty value """
        parsed = parseargs('')
        eq_(parsed, {})

        parsed = parseargs(' ')
        eq_(parsed, {})

        parsed = parseargs(None)
        eq_(parsed, {})

    def test_illigal(self):
        """ illigal value """
        parsed = parseargs('hoge')
        eq_(parsed, None)

        parsed = parseargs('hoge fuga')
        eq_(parsed, None)

        parsed = parseargs('hoge=1 fuga')
        print parsed
        eq_(parsed, None)

        parsed = parseargs(3)
        print parsed
        eq_(parsed, None)
