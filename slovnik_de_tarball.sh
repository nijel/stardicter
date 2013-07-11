#!/bin/sh
#
# Script to create tarballs of GNU/FDL Anglicko-Český slovník
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

set -e

# URL where to download source files
url='http://slovnik.hrach.eu/index.php?id=6&sablona=export&format=zcu'
NAME=stardict-german-czech
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
wget -O de-cs.txt -q $url
if [ ! -f de-cs.txt ] ; then
    echo "No file!"
    exit 1
fi
sed -i '/^# File generated/ D' de-cs.txt
NEWMD5=`md5sum de-cs.txt`
OLDMD5=`cat ~/.$NAME.md5 || true`
if [ "$NEWMD5" = "$OLDMD5" ] ; then
    exit 1
fi
echo "$NEWMD5" > ~/.$NAME.md5
cp de-cs.txt ../$dira
cp de-cs.txt ../$diran
cp de-cs.txt ../$dirn
python ../slovnik_de2stardict.py
dictzip *.dict
rm de-cs.txt
cd ..
tar cfz $dir.tar.gz $dir
rm -rf $dir
cd $dira
python ../slovnik_de2stardict.py --ascii
dictzip *.dict
rm de-cs.txt
cd ..
tar cfz $dira.tar.gz $dira
rm -rf $dira
cd $diran
python ../slovnik_de2stardict.py --ascii --notags
dictzip *.dict
rm de-cs.txt
cd ..
tar cfz $diran.tar.gz $diran
rm -rf $diran
cd $dirn
python ../slovnik_de2stardict.py --notags
dictzip *.dict
rm de-cs.txt
cd ..
tar cfz $dirn.tar.gz $dirn
rm -rf $dirn
