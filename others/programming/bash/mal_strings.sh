#!/bin/bash

string_path="/usr/bin/strings"
echo_path="/bin/echo"

for bin in $string_path $echo_path
do
        if [ ! -f "$bin" ]
        then
                echo "File: $bin Doesn't Exists On The System !!!"
                exit 1
        fi
done

if [ ! $# -eq 2 ]
then
        echo "Usage: $0 <file_path> <char_len>"
        exit 2
fi

mal_path="$1"
char_len="$2"

if [ ! -f "$mal_path" ]
then
        echo "File: '$mal_path' Doesn't Exists On The System !!!"
        exit 3
fi

echo "$char_len" | grep -qE "^[0-9]+$"
if [ ! $? -eq 0 ]
then
        echo "CharLen Must Be Integer !!!"
        exit 5
fi
 
$string_path "$mal_path"  | grep -vE "~|\!|\)|\&|\@|\*|\%|\(|\`|\#|\{|\}|\^|\]|\[|'|\s|\"|\;|\:|>|<|\+|\\\$|\,|\=|\?" | while read -r line
do 
        ch_len="`$echo_path -n "$line" | wc -c`"

        if [ $ch_len -gt $char_len ]
        then
                echo "$ch_len-$line"
        fi
done | sort -nr

exit 0
