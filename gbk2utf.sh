#!/bin/bash

function convert() {
    iconv --from-code="gbk" --to-code="utf8" -c -o $1.utf8 $1
}

function filter() {
    if [ $? -eq 0 ]; then
        convert $1
    fi
}

if [ $# -eq 0 ]; then
    echo "Usage: ./gbk2utf.sh filename" 
    exit
fi

if [ $1 == "-h" ]; then
    echo "Usage: ./gbk2utf.sh filename" 
    exit
fi

filter $1

