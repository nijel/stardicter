#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Convertor for Slovník cizích slov [1] to Stardict [2] format.

1. http://slovnik-cizich-slov.abz.cz/
2. http://stardict.sourceforge.net/
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__url__ = 'http://slovnik-cizich-slov.abz.cz/'
__license__ = '''
Copyright (c) 2006 - 2010 Michal Čihař

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License version 2 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''
__revision__ = '1.1'
__header__ = 'Slovník cizích slov to stardict convertor'
# silent pychecker
__pychecker__ = 'unusednames=__license__'

import sys
import struct
import datetime
import stardictcommon

# formatting:
# pronunciation
fmt_pronunciation = '[<i>%s</i>]\n\n'
# explanation text
fmt_explanation = '    %s\n'

def xmlescape(text):
    """escapes special xml entities"""
    return text\
        .replace('<', '&lt;')\
        .replace('>', '&gt;')\
        .replace('&', '&amp;')

def reformat(text):
    """cleanup usual junk found in words from database"""
    return text\
        .replace('\\"', '"')\
        .replace('\\\'', '\'')\
        .replace('\n', ' ')\
        .replace('\r', ' ')\
        .strip()

def formatentry(data):
    '''converts entry values from source to one string'''
    # sort alphabetically
    data.sort()
    # variables used for data
    result = '\n'
    index = 1
    # process all translations
    for item in data:
        if item[0] != '':
            result += fmt_pronunciation % xmlescape(item[0])
        for text in item[1].split(';'):
            it = (item[0], text)
            result += fmt_explanation % xmlescape(reformat(text))
            index += 1

    return result

def savelist(wlist, rev, filename = None):
    '''saves list of words to file, rev indicates whether it is forward or
    reversed direction'''

    # initialize variables
    offset = 0
    count = 0

    # which filename to use?
    if filename is None:
        filename = 'cz'

    # open all files
    dictf = open('%s.dict' % filename, 'w')
    idxf = open('%s.idx' % filename, 'w')
    ifof = open('%s.ifo' % filename, 'w')

    print 'Sorting %s...' % filename
    # case insensitive sort
    keys = list(wlist.keys())
    tuples = [(item.lower(), item) for item in keys]
    tuples.sort()
    keys = [item[1] for item in tuples]

    print 'Saving %s...' % filename
    for key in keys:
        # format single entry
        deftext = formatentry(wlist[key])

        # write dictionary text
        dictf.write(deftext)

        # write index entry
        idxf.write(key+'\0')
        idxf.write(struct.pack('!I', offset))
        idxf.write(struct.pack('!I', len(deftext)))

        # calculate offset for next index entry
        offset += len(deftext)
        count += 1

    # index size is needed in ifo
    idxsize = idxf.tell()

    # we're done with those two, close them
    dictf.close()
    idxf.close()

    # create ifo file
    ifof.write('StarDict\'s dict ifo file\n')
    ifof.write('version=2.4.2\n')
    ifof.write('bookname=Slovník cizích slov\n')
    ifof.write('wordcount=%d\n' % count)
    ifof.write('idxfilesize=%d\n' % idxsize)
    # There is no way to put all authors here, so I decided to put author of
    # convertor here :-)
    ifof.write('author=%s\n' % __author__)
    ifof.write('email=%s\n' % __email__)
    ifof.write('website=%s\n' % __url__)
    # we're using pango markup for all entries
    ifof.write('sametypesequence=g\n')
    today = datetime.date.today()
    ifof.write('date=%04d.%02d.%02d\n' % (today.year, today.month, today.day))
    ifof.close()

    print 'Saved %d words' % count




def loadslovnik(filename = 'slovnik.txt'):
    '''loads slovnik data into internal dictionary'''
    print 'Parsing dictionary...'

# open source file
    slovnik = open(filename)

# initialise data structures
    description = ''
    wordmap = {}
    revwordmap = {}
    count = 0

    while 1:
        line = slovnik.readline()
        if line == '':
            break
        # grab description
        if line[0] == '#':
            description += line[6:]
            continue
        # remove trailing \n
        line = line[:-1]
        # ignore empty lines
        if line.strip() == '':
            continue
        parts = line.split('|')
        try:
            word, pronunciation, explanation = parts
        except ValueError:
            print 'Invalid input: %s' % repr(line)
            sys.exit(1)
        # remove leading and trailing spaces, replace ugly chars
        explanation = reformat(explanation)
        word_list = word.split(',')
        explanation_list = explanation.split(',')
        for word in word_list:
            if word == '':
                continue
            # remove leading and trailing spaces, replace ugly chars
            word = reformat(word)
            for explanation in explanation_list:
                if explanation == '':
                    continue
                explanation = reformat(explanation)
                # forward dictionary
                try:
                    wordmap[word].append((pronunciation, explanation))
                except KeyError:
                    wordmap[word] = [(pronunciation, explanation)]
        # count words
        count += 1

    slovnik.close()
    print 'Parsed %d entries' % count
    return (wordmap, revwordmap, description)

if __name__ == '__main__':
    print '%s, version %s' % ( __header__, __revision__)
    # read data
    words, revwords, description = loadslovnik()
    # save description
    descf = open('README', 'w')
    descf.write('%s\n%s' % (
        stardictcommon.readme_en(
            'Czech foreign words dictionary',
            'http://slovnik-cizich-slov.abz.cz/',
            'unknown license',
            __header__,
            __revision__),
        stardictcommon.readme_cs(
            'Slovník cizích slov',
            'http://slovnik-cizich-slov.abz.cz/',
            'neznámou licencí',
            __header__,
            __revision__)))
    descf.close()
    # save data
    savelist(words, False)

