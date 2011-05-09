#!/bin/sh
#
# Script to create tarballs of GNU/FDL Anglicko-Český slovník
#
# Copyright (c) 2006 - 2011 Michal Čihař
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

set -e

# URL where to download source files
url='http://slovnik.zcu.cz/files/slovnik_data_utf8.txt.gz'
NAME=stardict-english-czech
dir="$NAME-`date +%Y%m%d`"
dira="$dir-ascii"
diran="$dir-ascii-notags"
dirn="$dir-notags"

rm -rf $dir $dira $dirn $diran
mkdir $dir
mkdir $dira
mkdir $dirn
mkdir $diran
cd $dir
wget -q $url
if [ ! -f slovnik_data_utf8.txt.gz ] ; then
    echo "No file!"
    exit 1
fi
if ! gunzip slovnik_data_utf8.txt.gz ; then
    echo 'Fail unzip!'
    exit 2
fi
sed -i '/^#      Date:/ D' slovnik_data_utf8.txt
NEWMD5=`md5sum slovnik_data_utf8.txt`
OLDMD5=`cat ~/.$NAME.md5 || true`
if [ "$NEWMD5" = "$OLDMD5" ] ; then
    exit 1
fi
echo "$NEWMD5" > ~/.$NAME.md5
cp slovnik_data_utf8.txt ../$dira
cp slovnik_data_utf8.txt ../$diran
cp slovnik_data_utf8.txt ../$dirn
python ../slovnik2stardict.py
dictzip *.dict
rm slovnik_data_utf8.txt
cd ..
tar cfz $dir.tar.gz $dir
rm -rf $dir
cd $dira
python ../slovnik2stardict.py --ascii
dictzip *.dict
rm slovnik_data_utf8.txt
cd ..
tar cfz $dira.tar.gz $dira
rm -rf $dira
cd $diran
python ../slovnik2stardict.py --ascii --notags
dictzip *.dict
rm slovnik_data_utf8.txt
cd ..
tar cfz $diran.tar.gz $diran
rm -rf $diran
cd $dirn
python ../slovnik2stardict.py --notags
dictzip *.dict
rm slovnik_data_utf8.txt
cd ..
tar cfz $dirn.tar.gz $dirn
rm -rf $dirn
