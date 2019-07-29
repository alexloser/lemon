#!/bin/bash
reset
github_dir=$PWD

if [ $# -ne 0 ]; then
    repos="$@"
else
    repos=`ls`
fi

for each in $repos
do
    if [ -d $each ]; then
        echo
        echo "------------["$each"]------------"
        cd $github_dir/$each
        git status | egrep -v "nothing to commit" | egrep -v "# On branch"
        cd ../
    fi
done

