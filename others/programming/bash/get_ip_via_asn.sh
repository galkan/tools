#!/bin/bash
# Galkan|Kastamonu
# Show Ip Address from domain using asn ...

prips_path="/usr/bin/prips"
host_path="/usr/bin/host"
whois_path="/usr/bin/whois"
dpkg_path="/usr/bin/dpkg"

domain=""
ip_list=0

if [ "$#" -eq 2 ] && [ "$1" == "-d" ]
then
        domain="$2"
elif [ "$#" -eq 4 ] && [ "$3" == "-i" ] && [ $4 -eq 0 -o $4 -eq 1 ]
then
        domain="$2"
        ip_list="$4"
else
        echo "Usage: $0 -d <domain> -i <1|0>"
        exit 1
fi

for cmd_file in $host_path $whois_path
do
        if [ ! -f $cmd_file ]
        then
                echo "File $cmd_file Doesn't Exists On The System."
                exit 1
        fi
done

if [ $ip_list -eq 1 ]
then
        if [ ! -f $prips_path ]
        then
                echo "File $prips_path Doesn't Exists On The System."
                exit 1
        fi
fi

ip_addr_file="`mktemp /tmp/$USER.XXXXXX`"
prefix_file="`mktemp /tmp/$USER.XXXXXX`"
whois_domain="asn.shadowserver.org"

function getip()
{
        domain="$1"

        host $domain | while read -r line
        do
                echo "$line" | grep -Eq "has address [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
                if [ $? -eq 0 ]
                then
                        echo $line | cut -d " " -f4 >> $ip_addr_file
                fi
done

if [ $ip_list -eq 1 ]
then
        if [ ! -f $prips_path ]
        then
                echo "File $prips_path Doesn't Exists On The System."
                exit 1
        fi
fi

ip_addr_file="`mktemp /tmp/$USER.XXXXXX`"
prefix_file="`mktemp /tmp/$USER.XXXXXX`"
whois_domain="asn.shadowserver.org"

function getip()
{
        domain="$1"

        host $domain | while read -r line
        do
                echo "$line" | grep -Eq "has address [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
                if [ $? -eq 0 ]
                then
                        echo $line | cut -d " " -f4 >> $ip_addr_file
                fi

                echo "$line" | grep -Eq "is handled by [0-9]+ "
                if [ $? -eq 0 ]
                then
                        new_domain="`echo $line | cut -d " " -f7`"
                        getip "$new_domain"
                fi
        done

}

getip "$domain"

sort -n $ip_addr_file | uniq | while read -r ip
do
        whois -h $whois_domain "origin $ip" | cut -d "|" -f1 | tr -d ' ' >> $prefix_file
done

sort -n $prefix_file | uniq | while read -r prefix
do
        if [ $ip_list -eq 1 ]
        then
                whois -h $whois_domain "prefix $prefix" | while read -r cidr
                do
                        $prips_path $cidr
                done
        else
                whois -h $whois_domain "prefix $prefix"
        fi
done

rm -rf $ip_addr_file $prefix_file
