#!/bin/sh
#
# Script to create tarballs of GNU/FDL Anglicko-Český slovník
#
# Copyright (c) 2006 Michal Čihař
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
url='http://slovnik.zcu.cz/files/slovnik_data_utf8.txt.gz'
dir="stardict-english-czech-`date +%Y%m%d`"

rm -rf $dir
mkdir $dir
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
python ../slovnik2stardict.py
dictzip *.dict
rm slovnik_data_utf8.txt
cd ..
tar cfj $dir.tar.bz2 $dir
rm -rf $dir
