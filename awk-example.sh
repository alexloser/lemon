#!/bin/bash

showtime() {
    date | cut -b 12-19
}

showtime
du -sh $1

egrep '.*?: .*?\.js(\W.*?)? http://.*' $1 |\
awk '{ 
	c[$3 " " $5]++; 
} 
END { 
	for(i in c) print c[i] ",", i; 
}' |\
awk ' BEGIN { 
	FS="?";
} 
{
	c[$1]++;
} 
END {
	for(i in c) print i;
}' |\
sort -nr > $2

showtime


