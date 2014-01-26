#!/bin/bash

if [ ! $# -eq 2 ]
then
        echo "Kullanim: $0 <rapor_dosyasi> <protokol>"
        exit 37
fi

nmap_rapor="$1"
proto="$2"

cat $nmap_rapor | grep “Ports” | while read -r line
do
        ip_addr="`echo "$line" | cut -d " " -f2`"
        control=0
        for line2 in `echo "$line" | cut -d " " -f4-`
        do
                echo "$line2" | grep -Eq "/$proto/"
                if [ $? -eq 0 ]
                then
                        if [ $control -eq 0 ]
                        then
                                echo "$ip_addr"
                                echo "-----------"
                                control=1
                        fi

                        port_number="`echo "$line2" | cut -d "/" -f1`"
                        service="`echo "$line2" | cut -d "/" -f5`"

                        echo "$port_number/$service"
                fi
        done
done

exit 0


---------------------------------
# ./nmap_raporlayici.sh rapor tcp
192.168.1.1
------------
21/ftp
22/ssh
80/http
443/https
192.168.1.23
------------
22/ssh
192.168.1.37
------------
80/http
139/netbios-ssn
443/https
445/microsoft-ds
