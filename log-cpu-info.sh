#!/bin/sh
#recored top info to cpu.log
#usage: sh logcpu.sh PID TIMES
#PID is the PID of process, TIMES is a number of recored times

if [ "$1" = "-h" ]; then
    echo "Usage: $0 PID TIMES"
    exit
elif [ $# -eq 0 ]; then
    echo "Usage: $0 PID TIMES"
    exit
fi

echo "USER PR NI VIRT S RES SHR %CPU %MEM TIME COMMAND"

i=0
while [ "$i" -le "$2" ];
do
    i=$((i+1));
    top -d 1 -n 1 -p "$1" | \
    awk '{if (NR>=8) {if (NF>13) {print $3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13} else {print $2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12}}}';
done
