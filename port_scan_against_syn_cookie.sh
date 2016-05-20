#!/bin/bash

if [ ! $# -eq 2 ]
then
        echo "Usage: $0 <Ip Address> <Port Number>"
        exit 1
fi

ip_range="$1"
port_number="$2"

nmap_path="/usr/bin/nmap"

if [ ! -f "$nmap_path" ]
then
        echo "\"$nmap_path\"  Doesn't Exists !!!"
        exit 1
fi


$nmap_path -n -sL $ip_range |  grep "Nmap scan report for" | cut -d " " -f5 | while read -r ip
do
        result_file="`mktemp /tmp/$USER.XXXXXX`"
        printf 'GET / HTTP/1.1\r\n\r\n' | nc $ip $port_number  >$result_file &

        sleep 3

        proc_pid="`ps -ef | grep -v grep | grep "nc $ip $port_number" | awk '{print $2}'`"

        if [ ! -z $proc_pid ]
        then
                kill -9 $proc_pid >/dev/null 2>&1
        fi

        line_count="`cat $result_file | grep -v "Connection reset by peer" | wc -l`"
        if [ $(( line_count )) -gt 2 ]
        then
                echo "$ip -> $port_number : OPENED"
        else
                echo "$ip -> $port_number : CLOSED"
        fi

        rm -rf $result_file

done
