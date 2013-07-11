#!/bin/sh
#
# Script to create tarballs of Czech-German dictionary
#
# Copyright (c) 2006 - 2013 Michal Čihař
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

if [ -z "$1" -o -z "$2" -o "x$1" = "x-h" -o "x$1" = "x--help" ] ; then
    echo "Usage: `basename $0` source-language target-language"
    exit 1
fi

source="$1"
target="$2"
source_u=`echo "$source" | sed -e 's/^./\U&/g'`
target_u=`echo "$target" | sed -e 's/^./\U&/g'`

# URL where to download source files
# This one used to work in past, now IP is required
url="http://www.dicts.info/uddl.php?l1=$source&l2=$target&format=text"
name="$source-$target"
reverse="$target-$source"
label="$source_u-$target_u dictionary"
reverselabel="$target_u-$source_u dictionary"
dir="stardict-$name-`date +%Y%m%d`"

rm -rf $dir
mkdir $dir
cd $dir
curl -d 'ok=selected' "$url" > $name.txt
if [ ! -f $name.txt ] ; then
    echo "No file!"
    exit 1
fi
python ../dictsinfo2stardict.py ./$name.txt "$label" "$reverselabel" $name $reverse
dictzip *.dict
rm $name.txt
cd ..
tar cfj $dir.tar.bz2 $dir
rm -rf $dir
