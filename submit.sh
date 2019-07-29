#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 message"
	exit
fi

echo $PWD

git commit -a -m $1
git push origin master

