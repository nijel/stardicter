#!/bin/sh
#
# Script to create tarballs of Czech-German dictionary
#
# Copyright (c) 2006 - 2007 Michal Čihař
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

# URL where to download source files
# This one used to work in past, now IP is required
#url='http://www.dicts.info/uddl.php?l1=czech&l2=german&format=text'
url='http://213.251.169.143/uddl.php?l1=czech&l2=german&format=text'
dir="stardict-czech-german-`date +%Y%m%d`"

rm -rf $dir
mkdir $dir
cd $dir
curl -d 'ok=selected' "$url" > czech-german.txt
if [ ! -f czech-german.txt ] ; then
    echo "No file!"
    exit 1
fi
python ../dictsinfo2stardict.py ./czech-german.txt 'Czech-German dictionary' 'German-Czech dictionary' cz-ge ge-cz
dictzip *.dict
rm czech-german.txt
cd ..
tar cfj $dir.tar.bz2 $dir
rm -rf $dir
