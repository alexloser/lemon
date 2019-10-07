#!/bin/bash
set -v
astyle --style=kr -k1 -j -p $1
