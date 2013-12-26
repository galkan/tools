#!/bin/bash

function get_ip()
{
	interface="$1"
	ip_addr="`ifconfig  $interface | grep 'inet add' | cut -d ':'  -f2 | awk '{print $1}'`"
	echo "$ip_addr"
}


function change_ip()
{
	interface="$1"

	dhclient_pid="`ps -ef | grep dhclient | grep -v grep | awk '{print $2}'`"
	if [ ! -z $dhclient_pid ]
	then
		kill -9 $dhclient_pid >/dev/null 2&>1
	fi	

	ip_addr="`get_ip "$interface"`"
	if [ ! -z $ip_addr ]
	then	
		echo "Old Ip Address: $ip_addr"
		ip addr del $ip_addr dev $interface  >/dev/null 2&>1
	fi
	
	ifconfig $interface down >/dev/null 2&>1
	macchanger --random $interface >/dev/null 2&>1
	
	ifconfig $interface up >/dev/null 2&>1
	dhclient $interface >/dev/null

	echo "New Ip Address: `get_ip "$interface"`"
	echo ""
}

##
### Main ...
##

interface="$1"
loop_count="$2"

if [ ! $# -eq 2 ]
then
	echo "Usage $0: <interface> <loop_count>"
	exit 1
fi	

control_file="`mktemp /tmp/$USER.XXXXXX`"
echo -e "0" > $control_file

for current_interface in `ifconfig -a | grep -Eo "^[^ ]+" | grep -v lo`
do
	if [ ! "$current_interface" == "$interface" ]
	then
		continue
	else
		echo -e "1" > $control_file
		break
	fi
done

if [ ! `cat $control_file` -eq 1 ]
then
	echo "There is no interface named -> $interface"
	rm -rf $control_file
	exit 2
fi
rm -rf $control_file

echo "$loop_count" | grep -Eq "^[0-9]+$"
if [ ! $? -eq 0 ]
then
	echo "Loop count must be integer -> $loop_count!!!"
	exit 3
fi

if [ ! $loop_count -eq 0 ]
then
	for count in `seq 1 $loop_count`
	do
		change_ip "$interface"
	done
else
	while [ 1 ]
	do
		change_ip "$interface"
	done
fi
