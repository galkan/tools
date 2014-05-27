#!/bin/bash

if [ ! $# -eq 1 ]
then
	echo "Usage: $0 <nmap_result_file>"
	exit 1
fi

tmp_file="`mktemp /tmp/$USER.XXXXXX`"
mac_addr="`mktemp /tmp/$USER.XXXXXX`"
device="`mktemp /tmp/$USER.XXXXXX`"
running="`mktemp /tmp/$USER.XXXXXX`"
os_cpe="`mktemp /tmp/$USER.XXXXXX`"
os_detail="`mktemp /tmp/$USER.XXXXXX`"

nmap_result_file="$1"
seperator="Nmap scan report for"

grep -n "$seperator" $nmap_result_file > $tmp_file
count="`wc -l $tmp_file | awk '{print $1}'`"

for x in `seq 2 $count`
do
	result="`cat $tmp_file | cut -d ":" -f1 | head -$x | tail -2`"
	first="`echo "$result" | head -1`"
	second="`echo "$result" | tail -1`"
	let "different = $second-$first-1"
	let "stop = $second-1"

	dns="`cat $tmp_file | cut -d ":" -f2 | head -$x | tail -1 | cut -d " " -f5`"
	echo "$dns" | grep -Eq "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
	if [ $? -eq 0 ]
	then
		ip_addr="`cat $tmp_file | cut -d ":" -f2 | head -$x | tail -1 | cut -d " " -f5`"
		dns="-"
	else
		ip_addr="`cat $tmp_file | cut -d ":" -f2 | head -$x | tail -1 | cut -d " " -f6 | tr -d "*(" | tr -d ")"`"
	fi

	head -$stop $nmap_result_file | tail -$different | while read -r line
	do
		for val in "MAC Address" "Device type" "Running" "OS CPE" "OS details"
		do	
			echo "$line" | grep -q "$val"
			if [ $? -eq 0 ]
			then
				case $val in 	"MAC Address" )
					echo "$line" | cut -d ":" -f2- | sed -e "s/^ //g" > $mac_addr ;;
					     	"Device type" )
					echo "$line" | cut -d ":" -f2- | sed -e "s/^ //g" > $device ;;
						"Running" )
					echo "$line" | cut -d ":" -f2- | sed -e "s/^ //g" > $running ;;
						"OS CPE" )
					echo "$line" | cut -d ":" -f2- | sed -e "s/^ //g" > $os_cpe ;;
						"OS details" )
					echo "$line" | cut -d ":" -f2- | sed -e "s/^ //g" > $os_detail ;;
				esac
				break
			fi	
		done
	done
	total_result="`cat $mac_addr`,`cat $device`,`cat $running`,`cat $os_cpe`,`cat $os_detail`"
	echo "$ip_addr,$dns,$total_result"	
done
rm -rf $tmp_file $mac_addr $device $running $os_cpe $os_detail
