#!/bin/bash

if [ ! $# -eq 3 ]
then
echo "Kullanim: $0 -r<sayi> -c<sayi> tablo.dat"
        exit 1
fi

row_opt="$1"
column_opt="$2"
table_file="$3"
table_file_count="`wc -l $table_file | awk '{print $1}'`"

for line in $row_opt $column_opt
do
echo "$line" | grep -Eq "^\-[r|c][0-9]+$"
        if [ ! $? -eq 0 ]
        then
echo "Yanlis Belirtim: $line, Satir veya Sutun Sayisi Belirtilmemis ->Ornek Kullanim: -r2|-c4"
                exit 2
        fi
done


if [ ! -f $table_file ]
then
echo "Dosya: $table_file Sistemde Bulunamadi !!!"
        exit 3
fi

row=""
column=""

echo "$row_opt" | grep -Eq "^\-r"
if [ $? -eq 0 ]
then
row="`echo "$row_opt" | cut -d "r" -f2`"
        column="`echo "$column_opt" | cut -d "c" -f2`"
else
row="`echo "$column_opt" | cut -d "r" -f2`"
        column="`echo "$row_opt" | cut -d "c" -f2`"
fi

if [ $row -gt $table_file_count ]
then
echo "Satir Sayisi: $row -> Dosyadaki Satir Sayisindan: $table_file_count -> Daha Fazla Olamaz !!!"
        exit 4
fi

counter=1
for count in `cat $table_file | head -$row | tail -1`
do
if [ $counter -eq $column ]
        then
echo "Sonuc: $count"
                break
fi

counter=$((counter+1))
done
