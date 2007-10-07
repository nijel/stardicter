#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: expandtab sw=4 ts=4 sts=4:
'''
Convertor for GNU/FDL Anglicko-Český slovník [1] to Stardict [2] format.

1. http://slovnik.zcu.cz/
2. http://stardict.sourceforge.net/

@todo handle priority in type field,  http://slovnik.zcu.cz/format.php
@todo include pronunciation,  http://slovnik.zcu.cz/format.php
'''
__author__ = u'Michal Čihař'
__email__ = 'michal@cihar.com'
__url__ = 'http://slovnik.zcu.cz/'
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
__revision__ = '1.2'
__header__ = 'GNU/FDL Anglicko-Český slovník to stardict convertor'
# silent pychecker
__pychecker__ = 'unusednames=__license__'

import sys
import struct
import datetime
import stardictcommon
import unicodedata
import codecs
import re
from optparse import OptionParser

# formatting:
# type of word (used as title)
fmt_type = u'<span size="larger" color="darkred" weight="bold">%s</span>\n'
# detailed type
fmt_details = u'<i>%s</i> '
# translation text
fmt_translate = u'<b>%s</b>'
# translation note
fmt_note = u' (%s)'
# translation author
fmt_author = u' <small>[%s]</small>'

striptags = re.compile(r"<.*?>", re.DOTALL)

opt_ascii = False
opt_notags = False

def deaccent(exc):
    if not isinstance(exc, UnicodeEncodeError):
        raise TypeError("don't know how to handle %r" % exc)
    l = []
    for c in exc.object[exc.start:exc.end]:
#        print '"%s" %d' % (c, ord(c))
        if c == u'\x93':
            l.append('"')
            continue
        elif c == u'\x94':
            l.append('"')
            continue
        elif c == u'\x92':
            l.append('\'')
            continue
        elif c == u'\x84':
            l.append('"')
            continue
        cat = unicodedata.category(c)
        name = unicodedata.name(c)
        if name[:18] == 'LATIN SMALL LETTER':
            l.append(unicode(name[19].lower()))
        elif name[:20] == 'LATIN CAPITAL LETTER':
            l.append(unicode(name[21]))
        elif name == 'ACUTE ACCENT':
            l.append('\'')
        elif name == 'MULTIPLICATION SIGN':
            l.append('x')
        elif name == 'DEGREE SIGN':
            l.append(' ')
        else:
            print c
            print cat
            print name
            raise exc
    return (u''.join(l), exc.end)

codecs.register_error('deaccent', deaccent)

def cvt(text):
    '''
    Converts text to match wanted format.
    '''
    if opt_ascii:
        text = text.encode('ascii', 'deaccent')

    if opt_notags:
        text = striptags.sub('', text)

    return text

def xmlescape(text):
    """escapes special xml entities"""
    return text\
        .replace('<', '&lt;')\
        .replace('>', '&gt;')\
        .replace('&', '&amp;')

def reformat(text):
    """cleanup usual junk found in words from database"""
    ret = text\
        .replace('\\"', '"')\
        .replace('\\\'', '\'')\
        .replace('\n', ' ')\
        .replace('\r', ' ')\
        .strip()
    return cvt(ret.decode('utf-8'))

def formatsingleentry(number, item):
    '''converts entry values from dictionary to one string'''
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
    # array for different word types
    alltypes = [
        'n:',
        'v:',
        'adj:',
        'adv:',
        'prep:',
        'conj:',
        'interj:',
        'num:',
        '',
    ]
    # variables used for data
    result = ''
    index = 1
    typed = {}
    # array holding typed words
    for key in alltypes:
        typed[key] = []
    # process all translations
    for item in data:
        tokens = item[1].split()
        saved = False
        for key in alltypes:
            # check if translation is current type
            if key in tokens:
                saved = True
                # remove type from translation, it will be in title
                del tokens[tokens.index(key)]
                newval = (item[0], u' '.join(tokens), item[2], item[3])
                # handle irregullar word specially (display them first)
                if '[neprav.]' in tokens:
                    backup = typed[key]
                    typed[key] = [newval]
                    typed[key] += backup
                else:
                    typed[key].append(newval)
                break
        if not saved:
            typed[''].append(item)

    # and finally convert entries to text
    for typ in alltypes:
        if len(typed[typ]) > 0:
            # header to display
            if typ == '':
                result += '\n'
            else:
                result += fmt_type % typ
            index = 1
            for item in typed[typ]:
                result += '    '
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

    # Are we generating ascii variant?
    if opt_ascii:
        filename = '%s-ascii' % filename
    # Are we generating notags variant?
    if opt_notags:
        filename = '%s-notags' % filename

    # open all files
    dictf = open('%s.dict' % filename, 'w')
    idxf = open('%s.idx' % filename, 'w')
    ifof = open('%s.ifo' % filename, 'w')

    print 'Sorting %s...' % filename
    # case insensitive sort
    keys = list(wlist.keys())
    tuples = [(item.encode('utf-8').lower(), item) for item in keys]
    tuples.sort()
    keys = [item[1] for item in tuples]

    print 'Saving %s...' % filename
    for key in keys:
        # format single entry
        deftext = cvt(formatentry(wlist[key]))

        # write dictionary text
        dictf.write(deftext.encode('utf-8'))

        # write index entry
        idxf.write(cvt(key).encode('utf-8')+'\0')
        idxf.write(struct.pack('!I', offset))
        idxf.write(struct.pack('!I', len(deftext.encode('utf-8'))))

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
        ifof.write(cvt(u'bookname=GNU/FDL Anglicko-Český slovník\n').encode('utf-8'))
    else:
        ifof.write(cvt(u'bookname=GNU/FDL Česko-Anglický slovník\n').encode('utf-8'))
    ifof.write('wordcount=%d\n' % count)
    ifof.write('idxfilesize=%d\n' % idxsize)
    # There is no way to put all authors here, so I decided to put author of
    # convertor here :-)
    ifof.write(cvt('author=%s\n' % __author__).encode('utf-8'))
    ifof.write(cvt('email=%s\n' % __email__).encode('utf-8'))
    ifof.write(cvt('website=%s\n' % __url__).encode('utf-8'))
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
            elif len(parts) < 5:
                while len(parts) < 5:
                    line += slovnik.readline()
                    parts = line.split('\t')
                print 'Fixup(<5): %s' % repr(line)
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
        if len(word) >= 256:
            print 'Ignoring word "%s", too long' % word
        else:
            try:
                wordmap[word].append((translation, wtype, note, author))
            except KeyError:
                wordmap[word] = [(translation, wtype, note, author)]
        # forward dictionary
        if len(translation) >= 256:
            print 'Ignoring reverse word "%s", too long' % repr(translation)
        else:
            try:
                revwordmap[translation].append((word, wtype, note, author))
            except KeyError:
                revwordmap[translation] = [(word, wtype, note, author)]
        # count words
        count += 1

    slovnik.close()
    print 'Parsed %d entries' % count
    return (wordmap, revwordmap, description)

if __name__ == '__main__':
    print '%s, version %s' % ( __header__, __revision__)

    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("", "--ascii",
                      action="store_true",
                      dest="ascii", default=False,
                      help="Generate plain ascii dictionary.")
    parser.add_option("", "--notags",
                      action="store_true",
                      dest="notags", default=False,
                      help="Generate dictionary without pango markup.")
    (options, args) = parser.parse_args()

    opt_ascii = options.ascii
    opt_notags = options.notags

    # read data
    words, revwords, description = loadslovnik()
    # save description
    descf = open('README', 'w')
    descf.write('%s\n%s' % (
        stardictcommon.readme_en(
            'English-Czech dictionary',
            'http://slovnik.zcu.cz/',
            'GNU/FDL license',
            __header__,
            __revision__),
        stardictcommon.readme_cs(
            'Anglicko-Český slovník',
            'http://slovnik.zcu.cz/',
            'licencí GNU/FDL',
            __header__,
            __revision__)))
    descf.write('\nOriginal description of dictionary:\n%s' % description)
    descf.close()
    # save data
    savelist(words, False)
    savelist(revwords, True)

