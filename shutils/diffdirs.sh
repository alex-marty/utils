#!/bin/bash

# Created on Fri 2016-04-01
# @author: Alexandre Marty <alexandre@marty.in>

# Shows a list of which files are different in dir1 and dir2, based on the
# filenames only and not the files' contents, unlike diff -r
# References:
# * http://stackoverflow.com/questions/19951883/du-counting-hardlinks-towards-filesize
# * https://raw.githubusercontent.com/joeytwiddle/jsh/HEAD/code/shellscript/file/diffdirs.sh

usage="$(basename "$0") [-h] dir1 dir2 -- show a list of files different between
    dir1 and dir2, based on filename"

DIR1="$1"
DIR2="$2"

if [ -z "$DIR1" ] || [ -z "$DIR2" ] || [ "$1" = "-h" ]; then
  echo "$usage"
  exit
fi

diff <(cd $DIR1 && find . | sort) <(cd $DIR2 && find . | sort)
