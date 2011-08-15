#!/usr/bin/env python
# encoding: utf-8;

from __future__ import with_statement

import os
import errno
import sys
import re
from optparse import OptionParser

class State(object):
    TEXT = 0
    UNORDERED_LIST = 1
    ORDERED_LIST = 2
    PREFORMATTED = 3
    EOF = 4

class TextProcessor(object):
    EOF = -1
    def __init__(self, text):
        self.text_ = text.expandtabs(4)
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
        # Return straight away if we're either in Preformatted mode, or the
        # line is shorter than the desired column length.
        if (len(self.line_) <= self.columns_ or
            self.state_ is State.PREFORMATTED):
            return []

        if self.state_ is State.PREFORMATTED:
            return []

        index = "".join(self.line_[:self.columns_]).rfind(' ')
        if index is not -1:
            if self.state_ in [State.TEXT, State.EOF]:
                self.output_.append("".join(self.line_[:index]).rstrip())
                self.line_ = self.line_[index+1:]
                self.wrapped_line_ = True
            elif self.state_ in [State.UNORDERED_LIST, State.ORDERED_LIST]:
                # TODO: ugly, cleanup.
                self.output_.append("".join(self.line_[:index]).rstrip())
                temp = self.line_[index+1:]
                self.line_ = [' ', ' ', ' ', ' ']
                self.line_.extend(temp)
                self.wrapped_line_ = True

    def columnize(self, text):
        proc = TextProcessor(text)
        
        self.reset()
        while not proc.eof():
            char = proc.next()
            # State changes only happen at the beginning and end of the
            # document, or at the beginning of a line after an empty line.
            if char is TextProcessor.EOF:
                self.state_ = State.EOF
            elif ((len(self.output_) is 0 and len(self.line_) is 0) or
                  (len(self.line_) is 0 and self.output_[-1] is "")):
                # Switch to unordered-list mode if the character is '*',
                # and the next character is whitespace.
                if char is '*' and proc.peek().isspace():
                    self.state_ = State.UNORDERED_LIST
                
                # Switch to ordered-list mode if the character is a series of
                # digits followed by a period, followed by a space.
                # elif TODO:
                #   self.state_ = State.UNORDERED_LIST

                # Switch to preformatted mode if the line starts with at least
                # four spaces.
                elif char.isspace() and proc.peek(3) == '   ':
                    print "Preformatted!"
                    self.state_ = State.PREFORMATTED
                else:
                    print "Char: '%s', Isspace: %s, Peek: '%s'" % (char, char.isspace(), proc.peek(3))
                    self.state_ = State.TEXT

            # When we hit the first space after the wrapping point, call
            # `wrap()` to process the current string, then add the
            # character.
            if ((self.state_ is State.EOF or char.isspace()) and
                len(self.line_) > self.columns_):
                self.wrap()

            if self.state_ in [State.TEXT, State.PREFORMATTED]:
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
            elif self.state_ is State.UNORDERED_LIST:
                if char == '*' and len(self.line_) is 0:
                    # Set up proper spacing
                    if len(self.output_) and self.output_[-1] is not "":
                        self.output_.append("")
                    self.line_ = [ '*', ' ', ' ', ' ']
                    while proc.peek().isspace():
                        proc.next()
                elif char == '\n':
                    if len(self.line_) is 0 and self.output_[-1] is "":
                        self.state_ = State.TEXT
                    self.output_.append("".join(self.line_).rstrip())
                    self.line_ = []
                else:
                    self.line_.append(char)

        self.output_.append("".join(self.line_).rstrip())
        return "\n".join(self.output_).rstrip()

def main(argv=None):
    if argv is None:
        argv = sys.argv

    default_root = os.path.dirname(os.path.abspath(__file__))

    parser = OptionParser(usage="Usage: %prog [options]", version="%prog 0.1")
    parser.add_option("--verbose",
                      action="store_true",
                      dest="verbose_mode",
                      default=False,
                      help="Verbose mode")

    parser.add_option("-i", "--input",
                      action="store",
                      dest="input",
                      default=None,
                      help="Which file should be processed? Defaults to stdin if no input file is provided.")

    parser.add_option("-c", "--columns",
                      action="store",
                      dest="columns",
                      default=80,
                      help="How many columns should the output file contain?")

    (options, args) = parser.parse_args()

    if options.input:
        with open(options.input, 'r') as f:
            text = f.read().rstrip()
    else:
        text = sys.stdin.read().rstrip()
    c = Columnizer(cols=options.columns)
    print c.columnize(text)
 

if __name__ == "__main__":
    sys.exit(main())
