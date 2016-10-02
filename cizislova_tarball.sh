#!/bin/sh
#
# Script to create tarballs of Slovník cizích slov
#
# Copyright (c) 2006 - 2016 Michal Čihař
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

NAME=stardict-czech
dir="$NAME-`date +%Y%m%d`"

if [ "x$1" = 'x--wrap' ] ; then
    WRAP="$2"
    shift 2
fi

rm -rf $dir
mkdir $dir

$WRAP ./sdgen.py --change --directory $dir "$@" czech

if [ ! -f $dir/README ] ; then
    rm -rf $dir
    exit 0
fi

# Compress
dictzip $dir/*.dict

# Create tarball
tar --owner=root --group=root --numeric-owner -czf $dir.tar.gz $dir
rm -rf $dir
