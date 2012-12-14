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
        test_key = 'test_key'

        test_value = 'hoge'
        parsed = parseargs(test_value)
        eq_(parsed, {})
        parsed = parseargs(test_value, default_key=test_key)
        eq_(parsed.get(test_key), test_value)

        test_value = 'hoge fuga'
        parsed = parseargs(test_value)
        eq_(parsed, {})
        parsed = parseargs(test_value, default_key=test_key)
        eq_(parsed.get(test_key), test_value)

        test_value = 'hoge=1 fuga'
        parsed = parseargs(test_value)
        eq_(parsed, {})
        parsed = parseargs(test_value, default_key=test_key)
        eq_(parsed.get(test_key), test_value)

        test_value = 23
        parsed = parseargs(test_value)
        eq_(parsed, {})
        parsed = parseargs(test_value, default_key=test_key)
        eq_(parsed.get(test_key), test_value)
