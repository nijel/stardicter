#!/bin/sh
#
# Script to create tarballs of Slovník cizích slov
#
# Copyright (c) 2006 - 2011 Michal Čihař
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.

# URL where to download source files
url='http://slovnik-cizich-slov.abz.cz/export.php'
NAME=stardict-czech
dir="$NAME-`date +%Y%m%d`"


rm -rf $dir
mkdir $dir
cd $dir
wget -q $url
if [ ! -f export.php ] ; then
    echo "No file!"
    exit 1
fi
mv export.php slovnik.txt
NEWMD5=`md5sum slovnik.txt`
OLDMD5=`cat ~/.$NAME.md5 || true`
if [ "$NEWMD5" = "$OLDMD5" ] ; then
    exit 1
fi
echo "$NEWMD5" > ~/.$NAME.md5
recode iso-8859-2..utf-8 slovnik.txt
python ../cizislova2stardict.py
dictzip *.dict
rm slovnik.txt
cd ..
tar cfz $dir.tar.gz $dir
rm -rf $dir
