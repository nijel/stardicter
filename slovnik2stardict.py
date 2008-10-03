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
FMT_TYPE = u'<span size="larger" color="darkred" weight="bold">%s</span>\n'
# detailed type
FMT_DETAILS = u'<i>%s</i> '
# translation text
FMT_TRANSLATE = u'<b>%s</b>'
# translation note
FMT_NOTE = u' (%s)'
# translation author
FMT_AUTHOR = u' <small>[%s]</small>'

BOOK_EN_CZ = u'GNU/FDL Anglicko-Český slovník'
BOOK_CZ_EN = u'GNU/FDL Česko-Anglický slovník'

STRIPTAGS = re.compile(r"<.*?>", re.DOTALL)

class Params:
    '''
    Parameters storage class.
    '''

    _ascii = False
    _notags = False

    def __init__(self, ascii = None, notags = None):
        '''
        Creates new parameters object.
        '''
        if ascii is not None:
            self._ascii = ascii
        if notags is not None:
            self._notags = notags

    def get_ascii(self):
        '''
        Returns value of ascii configuration option.
        '''
        return self._ascii

    def get_notags(self):
        '''
        Returns value of notags configuration option.
        '''
        return self._notags

def deaccent(exc):
    '''
    Removes accents on string conversion errors.
    '''
    if not isinstance(exc, UnicodeEncodeError):
        raise TypeError("don't know how to handle %r" % exc)
    result = []
    for current in exc.object[exc.start:exc.end]:
#        print '"%s" %d' % (current, ord(current))
        if current == u'\x93':
            result.append('"')
            continue
        elif current == u'\x94':
            result.append('"')
            continue
        elif current == u'\x92':
            result.append('\'')
            continue
        elif current == u'\x84':
            result.append('"')
            continue
        cat = unicodedata.category(current)
        name = unicodedata.name(current)
        if name[:18] == 'LATIN SMALL LETTER':
            result.append(unicode(name[19].lower()))
        elif name[:20] == 'LATIN CAPITAL LETTER':
            result.append(unicode(name[21]))
        elif name == 'ACUTE ACCENT':
            result.append('\'')
        elif name == 'NO-BREAK SPACE':
            result.append(' ')
        elif name == 'MULTIPLICATION SIGN':
            result.append('x')
        elif name == 'DEGREE SIGN':
            result.append('<degree>)')
        elif name == 'SECTION SIGN':
            # §
            result.append('<paragraph>')
        else:
            try:
                print current
            except UnicodeEncodeError:
                print repr(current)
            print cat
            print name
            raise exc
    return (u''.join(result), exc.end)

codecs.register_error('deaccent', deaccent)

def cvt(params, text):
    '''
    Converts text to match wanted format.
    '''
    if params.get_ascii():
        text = text.encode('ascii', 'deaccent')

    if params.get_notags():
        text = STRIPTAGS.sub('', text)

    return text

def xmlescape(text):
    """escapes special xml entities"""
    return text\
        .replace('<', '&lt;')\
        .replace('>', '&gt;')\
        .replace('&', '&amp;')

def reformat(params, text):
    """cleanup usual junk found in words from database"""
    ret = text\
        .replace('\\"', '"')\
        .replace('\\\'', '\'')\
        .replace('\n', ' ')\
        .replace('\r', ' ')\
        .strip()
    return cvt(params, ret.decode('utf-8'))

def formatsingleentry(item):
    '''converts entry values from dictionary to one string'''
    result = ''
    if item[1] != '':
        result += FMT_DETAILS % xmlescape(item[1])
    result += FMT_TRANSLATE % xmlescape(item[0])
    if item[2] != '':
        result += FMT_NOTE % xmlescape(item[2])
    if item[3] != '':
        result += FMT_AUTHOR % xmlescape(item[3])
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
                result += FMT_TYPE % typ
            for item in typed[typ]:
                result += '    '
                result += formatsingleentry(item)

    return result

def getsortedkeys(inputlist):
    '''
    Returns keys of hash sorted case insensitive.
    '''
    keys = list(inputlist.keys())
    tuples = [(item.encode('utf-8').lower(), item) for item in keys]
    tuples.sort()
    return [item[1] for item in tuples]

def savelist(params, wlist, rev, filename = None):
    '''
    Saves list of words to file, rev indicates whether it is forward or
    reversed direction.
    '''

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
        if params.get_ascii():
            filename = '%s-ascii' % filename

        # Are we generating notags variant?
        if params.get_notags():
            filename = '%s-notags' % filename

    # open all files
    dictf = open('%s.dict' % filename, 'w')
    idxf = open('%s.idx' % filename, 'w')
    ifof = open('%s.ifo' % filename, 'w')

    print 'Saving %s...' % filename
    for key in getsortedkeys(wlist):
        # format single entry
        deftext = cvt(params, formatentry(wlist[key]))

        # write dictionary text
        entry = deftext.encode('utf-8')
        dictf.write(entry)

        # write index entry
        idxf.write(cvt(params, key).encode('utf-8')+'\0')
        idxf.write(struct.pack('!I', offset))
        idxf.write(struct.pack('!I', len(entry)))

        # calculate offset for next index entry
        offset += len(entry)
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
        name = BOOK_EN_CZ
    else:
        name = BOOK_CZ_EN
    ifof.write(cvt(params, u'bookname=%s\n' % name).encode('utf-8'))
    ifof.write('wordcount=%d\n' % count)
    ifof.write('idxfilesize=%d\n' % idxsize)
    # There is no way to put all authors here, so I decided to put author of
    # convertor here :-)
    ifof.write(cvt(params, 'author=%s\n' % __author__).encode('utf-8'))
    ifof.write(cvt(params, 'email=%s\n' % __email__).encode('utf-8'))
    ifof.write(cvt(params, 'website=%s\n' % __url__).encode('utf-8'))
    # we're using pango markup for all entries
    ifof.write('sametypesequence=g\n')
    today = datetime.date.today()
    ifof.write('date=%04d.%02d.%02d\n' % (today.year, today.month, today.day))
    ifof.close()

    print 'Saved %d words' % count


def parse_line(params, slovnik, line):
    '''
    Fixes up broken input line.
    '''
    # split it up
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
    word = reformat(params, word)
    translation = reformat(params, translation)
    wtype = reformat(params, wtype)
    note = reformat(params, note)
    author = reformat(params, author)

    return (word, translation, wtype, note, author)

def loadslovnik(params, filename = 'slovnik_data_utf8.txt'):
    '''
    Loads slovnik data into internal dictionary.
    '''
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

        word, translation, wtype, note, author = \
            parse_line(params, slovnik, line)

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

def main():
    '''
    Main script code.
    '''
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

    params = Params(options.ascii, options.notags)

    # read data
    words, revwords, description = loadslovnik(params)
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
    savelist(params, words, False)
    savelist(params, revwords, True)

if __name__ == '__main__':
    main()
