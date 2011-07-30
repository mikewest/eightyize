#!/usr/bin/env python
# encoding: utf-8;

from __future__ import with_statement

import os
import errno
import sys
import re

class Columnizer(object):
    def __init__(self, cols = 80):
        self.text_ = ""
        self.columns_ = cols

    def columnize(self, text):
        self.output_ = []
        self.line_ = []
        self.wrapped_line_ = False
        for char in text:
            print "Line: '%s'" % "".join(self.line_)
            if char.isspace() and len(self.line_) > self.columns_:
                self.wrap()
            if char == '\n':
                print "Newline!"
                temp = "".join(self.line_).rstrip()
                if not self.wrapped_line_ or len(temp) > 0:
                    self.output_.append("".join(self.line_).rstrip())
                self.line_ = []
                self.wrapped_line_ = False
            else:
                print "Normal."
                self.line_.append(char)
        if len(self.line_) > self.columns_:
            self.wrap()
        self.output_.append("".join(self.line_).rstrip())
        return "\n".join(self.output_).rstrip()

    def wrap(self):
        if len(self.line_) <= self.columns_:
            return []

        index = "".join(self.line_).rfind(' ')
        if index is not -1:
            self.output_.append("".join(self.line_[:index]).rstrip())
            self.line_ = self.line_[index+1:]
            self.wrapped_line_ = True
