#!/bin/bash

[[ $# -lt 1 ]] && echo usage: $0 "[energy.dat]" && exit 1

cat /dev/null > tmpNRG.dat

totalE=(`tail -n+2 $1 | awk '{print $2}'`)

c=0

for i in `seq -w 2.0 0.05 8.0`; do
	printf "%f\t%f\n" "$i" "${totalE[$c]}" >> tmpNRG.dat
	((c++))
done

[ "$2" != "noplot" ] && xmgrace tmpNRG.dat

prefix=`echo $1 | cut -d . -f1`
cp tmpNRG.dat $prefix.xmgrace.dat
rm tmpNRG.dat

