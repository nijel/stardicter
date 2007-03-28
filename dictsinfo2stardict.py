#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Convertor for Dicts.info [1] to Stardict [2] format.

1. http://www.dicts.info/
2. http://stardict.sourceforge.net/
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__url__ = 'http://www.dicts.info/'
__license__ = '''
Copyright (c) 2006 - 2007 Michal Čihař

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
__header__ = 'Dicts.info to stardict convertor'
# silent pychecker
__pychecker__ = 'unusednames=__license__'

import sys
import struct
import datetime
import stardictcommon

# formatting:
# type of word (used as title)
fmt_type = '<span size="larger" color="darkred" weight="bold">%s</span>\n'
# detailed type
fmt_details = '<i>%s</i> '
# translation text
fmt_translate = '<b>%s</b>'
# translation note
fmt_note = ' (%s)'
# translation author
fmt_author = ' <small>[%s]</small>'

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

def formatsingleentry(number, item):
    '''converts entry values from dictionary to one string'''
    result = '<span size="small" foreground="darkblue">%d.</span> ' % number
    result = ''
    result += fmt_translate % xmlescape(item[0])
    result += '\n'
    return result

def formatentry(data):
    '''converts entry values from source to one string'''
    # sort alphabetically
    data.sort()
    # variables used for data
    result = ''
    index = 1
    lasttype = ''
    result += '\n'
    # process all translations
    for item in data:
        if lasttype != item[1]:
            # header to display
            if item[1] == '':
                result += '\n'
            else:
                result += fmt_type % item[1]
            lasttype = item[1]
            index = 1
        result += '    '
        result += formatsingleentry(index, item)
        index += 1

    return result

def savelist(wlist, rev, name, filename = None):
    '''saves list of words to file, rev indicates whether it is forward or
    reversed direction'''

    # initialize variables
    offset = 0
    count = 0

    # which filename to use?
    if filename is None:
        if rev:
            filename = 'czen'
        else:
            filename = 'encz'

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
    if rev:
        ifof.write('bookname=%s\n' % name)
    else:
        ifof.write('bookname=%s\n' % name)
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




def loadslovnik(filename):
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
        # remove trailing \n, spaces, \t
        line = line.strip()
        # ignore empty lines
        if line == '':
            continue
        parts = line.split('\t')
        type = ''
        try:
            words, translations, type = parts
        except ValueError:
            try:
                words, translations = parts
            except ValueError:
                print 'Invalid input: %s' % repr(line)
                sys.exit(1)
        # remove leading and trailing spaces, replace ugly chars
        words = reformat(words)
        translations = reformat(translations)
        # ignore non translated words
        if words == '' or translations == '':
            continue
        # split to words
        word_list = words.split(';')
        translation_list = translations.split(';')
        for word in word_list:
            word = word.strip()
            for translation in translation_list:
                translation = translation.strip()
                # generate inversed dictionary on the fly
                try:
                    revwordmap[translation].append((word, type))
                except KeyError:
                    revwordmap[translation] = [(word, type)]
                # forward dictionary
                try:
                    wordmap[word].append((translation, type))
                except KeyError:
                    wordmap[word] = [(translation, type)]
        # count words
        count += 1

    slovnik.close()
    print 'Parsed %d entries' % count
    return (wordmap, revwordmap, description)

if __name__ == '__main__':
    print '%s, version %s' % ( __header__, __revision__)
    if len(sys.argv) != 6:
        print 'Usage: dictsinfo2stardict.py <input file> <dictionary name> <reverse dictionary name> <output filename> <output filename rev>'
        sys.exit(1)
    # read data
    words, revwords, description = loadslovnik(sys.argv[1])
    # save description
    descf = open('README', 'w')
    descf.write(
        stardictcommon.readme_en(
            sys.argv[2],
            'http://dicts.info/',
            'unknown license',
            __header__,
            __revision__))
    descf.close()
    # save data
    savelist(words, False, sys.argv[2], sys.argv[4])
    savelist(revwords, True, sys.argv[3], sys.argv[5])

