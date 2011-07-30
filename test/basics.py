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

    def columnize(self, name, msg):
        self.getFixtures(name)
        self.assertEqual(self.out_, self.cols_.columnize(self.in_), msg)
#
# Plain text
#
    def test_empty(self):
        self.columnize('00-empty', 
                       'Columnizing an empty string returns an empty string')

    def test_oneline_short(self):
        self.columnize('01-oneline-short',
                       ('Columnizing an 80 character string returns '
                        'the same string'))

    def test_oneline_long(self):
        self.columnize('02-oneline-long',
                  ('Columnizing a 80+ character string returns multiple 80- '
                   'character strings'))

    def test_whitespace(self):
        self.columnize('03-whitespace',
                       'Lines should be stripped of trailing whitespace.')

    def test_multiline_short(self):
        self.columnize('04-multiline-short',
                       'Lines under 80 characters should remain the same.')

    def test_multiline_long(self):
        self.columnize('05-multiline-long',
                       'Lines over 80 characters should be wrapped.')
