#!/usr/bin/env python
# encoding: utf-8;

import unittest
import os, sys

TESTROOT = os.path.dirname( os.path.abspath( __file__ ) )
FIXTURES = os.path.join( TESTROOT, 'fixtures' )

libpath = [ os.path.join( TESTROOT, '..', 'src' ) ]
libpath.extend( sys.path )
sys.path = libpath

from eighty import Columnizer
 
class TestColumnizer(unittest.TestCase):
    def setUp(self):
        self.cols_ = Columnizer(80)

    def getFixtures(self, name):
        """Intentionally ignoring trailing whitespace."""
        self.in_ = ''
        self.out_ = ''
        with open(os.path.join(FIXTURES, name, 'input.txt'), 'r') as f:
            self.in_ = f.read().rstrip()
        with open(os.path.join(FIXTURES, name, 'expected.txt'), 'r') as f:
            self.out_ = f.read().rstrip()

    def debugPrint(self, text):
        return text.replace(' ', '+').replace('\n', '\\n\n')

    def columnize(self, name, msg):
        self.getFixtures(name)
        print '\n>>> Expected:\n%s\n\n>>> Actual:\n%s' % (
                self.debugPrint(self.out_),
                self.debugPrint(self.cols_.columnize(self.in_)))
        self.assertEqual(self.out_, self.cols_.columnize(self.in_), msg)

#
# Unit Tests
#
    def test_wrap(self):
        # Shorter columns for easier testing
        col = Columnizer(10)
        col.line_ = '0 2 4 6 8 0 '
        col.wrap()
        self.assertEqual('0 ', col.line_)

        col.line_ = '0 2 4 6 8 0'
        col.wrap()
        self.assertEqual('0', col.line_)

        col.line_ = '0 2 4 6 8 '
        col.wrap()
        self.assertEqual('0 2 4 6 8 ', col.line_)

#
# Plain text
#
    def test_empty(self):
        self.columnize('empty', 
                       'Columnizing an empty string returns an empty string')

    def test_oneline_short(self):
        self.columnize('oneline-short',
                       ('Columnizing an 80 character string returns '
                        'the same string'))

    def test_oneline_long(self):
        self.columnize('oneline-long',
                  ('Columnizing a 80+ character string returns multiple 80- '
                   'character strings'))

    def test_whitespace(self):
        self.columnize('whitespace',
                       'Lines should be stripped of trailing whitespace.')

    def test_multiline_short(self):
        self.columnize('multiline-short',
                       'Lines under 80 characters should remain the same.')

    def test_multiline_long(self):
        self.columnize('multiline-long',
                       'Lines over 80 characters should be wrapped.')

    def test_tabs(self):
        self.columnize('tabs',
                       'Tabs should be expanded to four spaces.')

#
# Markdown
#
    def test_unordered_list(self):
        self.columnize('unordered-list',
                       'Unordered lists should be properly wrapped.')

    def test_unordered_list_multiple(self):
        self.columnize('unordered-list-multiple',
                       ('Multiple unordered list items should be properly '
                        'wrapped.'))

    def test_unordered_list_multiple_nospace(self):
        self.columnize('unordered-list-multiple-nospace',
                       ('Multiple unordered list items without breaking '
                        'newlinesshould be properly wrapped.'))

    def test_unordered_list_then_text(self):
        self.columnize('unordered-list-then-text',
                       'Multiple unordered list items with normal text.')

    def test_text_then_pre(self):
        self.columnize('text-then-pre',
                       'Text followed by preformatted text.')

    def test_text_then_multiline_pre(self):
        self.columnize('text-then-multiline-pre',
                       'Text followed by multiple lines of preformatted text.')
