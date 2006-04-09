#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Convertor for GNU/FDL Anglicko-Český slovník [1] to Stardict [2] format.

1. http://slovnik.zcu.cz/
2. http://stardict.sourceforge.net/
'''
__author__ = 'Michal Čihař'
__email__ = 'michal@cihar.com'
__url__ = 'http://slovnik.zcu.cz/'
__license__ = '''
Copyright (c) 2006 Michal Čihař

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
__revision__ = '1.0'
__header__ = 'GNU/FDL Anglicko-Český slovník to stardict convertor'
# silent pychecker
__pychecker__ = 'unusednames=__license__'

import sys
import struct
import datetime

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
    if item[1] != '':
        result += fmt_details % xmlescape(item[1])
    result += fmt_translate % xmlescape(item[0])
    if item[2] != '':
        result += fmt_note % xmlescape(item[2])
    if item[3] != '':
        result += fmt_author % xmlescape(item[3])
    result += '\n'
    return result

def formatentry(data):
    '''converts entry values from source to one string'''
    # sort alphabetically
    data.sort()
    result = ''
    index = 1
    # array for different word types
    typed = {
        'n:':[],
        'v:':[],
        'adj:':[],
        'adv:':[],
        'prep:':[],
        'conj:':[],
        'interj:':[],
        'num:':[],
    }
    nottyped = []
    types = []
    for item in data:
        tokens = item[1].split()
        saved = False
        for key in typed.keys():
            for i in range(len(tokens)):
                if tokens[i] == '%s' % key:
                    if not key in types:
                        types.append(key)
                    saved = True
                    del tokens[i]
                    newval = (item[0], ' '.join(tokens), item[2], item[3])
                    # handle irregullar word specially
                    if '[neprav.]' in tokens:
                        backup = typed[key]
                        typed[key] = [newval]
                        typed[key] += backup
                    else:
                        typed[key].append(newval)
                    break
            if saved:
                break
        if not saved:
            nottyped.append(item)
            if not '' in types:
                types.append('')

    for typ in typed:
        if len(typed[typ]) > 0:
            prepend = ''
            if len(types) + len(nottyped) > 1:
                result += fmt_type % typ
                prepend = '   '
            index = 1
            for item in typed[typ]:
                result += prepend
                result += formatsingleentry(index, item)
                index += 1

    if len(nottyped) > 0:
        prepend = ''
        if len(types) > 1:
            result += '\n'
            prepend = '   '
        index = 1
        for item in nottyped:
            result += prepend
            result += formatsingleentry(index, item)
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
        ifof.write('bookname=GNU/FDL Anglicko-Český slovník\n')
    else:
        ifof.write('bookname=GNU/FDL Česko-Anglický slovník\n')
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




def loadslovnik(filename = 'slovnik_data_utf8.txt'):
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
        parts = line.split('\t')
        try:
            word, translation, wtype, note, author = parts
        except ValueError:
            if len(parts) == 6:
                print 'Fixup(6): %s' % repr(line)
                word, ignore, translation, wtype, note, author = parts
                word += ignore
            elif len(parts) == 2:
                while len(parts) < 5:
                    line += slovnik.readline()
                    parts = line.split('\t')
                print 'Fixup(2): %s' % repr(line)
                word, translation, wtype, note, author = parts
            else:
                print 'Invalid input: %s' % repr(line)
                sys.exit(1)
        # remove leading and trailing spaces, replace ugly chars
        word = reformat(word)
        translation = reformat(translation)
        wtype = reformat(wtype)
        note = reformat(note)
        author = reformat(author)
        # ignore non translated words
        if word == '' or translation == '':
            continue
        # generate inversed dictionary on the fly
        try:
            revwordmap[translation].append((word, wtype, note, author))
        except KeyError:
            revwordmap[translation] = [(word, wtype, note, author)]
        # forward dictionary
        try:
            wordmap[word].append((translation, wtype, note, author))
        except KeyError:
            wordmap[word] = [(translation, wtype, note, author)]
        # count words
        count += 1

    slovnik.close()
    print 'Parsed %d entries' % count
    return (wordmap, revwordmap)

if __name__ == '__main__':
    print '%s, version %s' % ( __header__, __revision__)
    # read data
    words, revwords = loadslovnik()
    # save data
    savelist(words, False)
    savelist(revwords, True)

