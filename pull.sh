#!/bin/bash

github_dir=$PWD

if [ $# -ne 0 ]; then
    repos="$@"
else
    repos=`ls`
fi

# echo $repos

for each in $repos
do
    if [ -d $each ]; then
        echo $each
        cd $github_dir/$each
        git pull &
        cd ../
        echo
    fi
done

wait
echo "Done"
