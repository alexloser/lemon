#!/bin/bash

addr="https://github.com/alexloser"

for name in "$@"
do
    git clone $addr/$name &
    echo
done
wait

