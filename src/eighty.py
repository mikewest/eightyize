#!/usr/bin/env python
# encoding: utf-8;

from __future__ import with_statement

import os
import errno
import sys
import re

class State(object):
    TEXT = 0
    UNORDERED_LIST = 1
    ORDERED_LIST = 2
    EOF = 3

class TextProcessor(object):
    EOF = -1
    def __init__(self, text):
        self.text_ = text
        self.max_pos_ = len(self.text_)
        self.index_ = -1
        
    def next(self):
        self.index_ += 1
        if not self.eof():
            return self.text_[self.index_]
        else:
            return TextProcessor.EOF

    def peek(self, x = 1):
        return self.text_[self.index_+1:self.index_+1+x]

    def eof(self):
        return self.index_ >= self.max_pos_

class Columnizer(object):
    def __init__(self, cols = 80):
        self.columns_ = cols
        self.reset()

    def reset(self):
        self.state_ = State.TEXT
        self.text_ = ''
        self.line_ = []
        self.output_ = []
        self.wrapped_line_ = False

    def wrap(self):
        if len(self.line_) <= self.columns_:
            return []

        index = "".join(self.line_[:self.columns_]).rfind(' ')
        if index is not -1:
            self.output_.append("".join(self.line_[:index]).rstrip())
            self.line_ = self.line_[index+1:]
            self.wrapped_line_ = True

    def columnize(self, text):
        proc = TextProcessor(text)
        
        self.reset()
        while not proc.eof():
            char = proc.next()
            # State changes only happen at the beginning and end of the
            # document, or at the beginning of a line after an empty line.
            if char is TextProcessor.EOF:
                state = State.EOF
            elif ((len(self.output_) is 0 and len(self.line_) is 0) or
                  (len(self.line_) is 0 and self.output_[-1] is "")):
                print "switchable"
                # Switch to unordered-list mode if the character is '*',
                # and the next character is whitespace.
                print "%d, %s, %s" % (len(self.line_), char, proc.peek())
                if (len(self.line_) is 0 and char is '*' and
                    proc.peek().isspace()):
                    state = State.UNORDERED_LIST
                else:
                    state = State.TEXT

            # When we hit the first space after the wrapping point, call
            # `wrap()` to process the current string, then add the
            # character.
            if (state is State.EOF or char.isspace()) and len(self.line_) > self.columns_:
                self.wrap()

            if state is State.TEXT:
                # If we've grabbed a newline character, we're done with this
                # line. Strip trailing whitespace, save it off and start
                # another. Don't append this newline to the output if we've
                # just wrapped a line. Otherwise we'll end up with doubles.
                if char == '\n':
                    line = "".join(self.line_).rstrip()
                    if not self.wrapped_line_ or len(line) > 0:
                        self.output_.append(line)
                    self.line_ = []
                    self.wrapped_line_ = False
                # If we've grabbed anything other than a newline, append it
                # to the current line, and move on to the next character.
                else:
                    self.line_.append(char)
            elif state is State.UNORDERED_LIST:
                if char is '*' and len(self.line_) is 0:
                    # Set up proper spacing
                    self.line = "*   "
                    while proc.peek().isspace():
                        proc.next()
                state = State.TEXT

        self.output_.append("".join(self.line_).rstrip())
        return "\n".join(self.output_).rstrip()
"""
        self.output_ = []
        self.line_ = []
        self.wrapped_line_ = False
        
        state = State.TEXT

        for char in text:
            if char.isspace() and len(self.line_) > self.columns_:
                self.wrap()
            if char == '\n':
                temp = "".join(self.line_).rstrip()
                if not self.wrapped_line_ or len(temp) > 0:
                    self.output_.append("".join(self.line_).rstrip())
                self.line_ = []
                self.wrapped_line_ = False
            else:
                self.line_.append(char)
        if len(self.line_) > self.columns_:
            self.wrap()
        self.output_.append("".join(self.line_).rstrip())
        return "\n".join(self.output_).rstrip()
"""

